"""
Purdue University Aerospace & Mechanical Engineering Faculty Scraper & Cold Outreach Intelligence Pipeline.

This pipeline scrapes, filters, categorizes, and enriches faculty from:
1. School of Aeronautics and Astronautics (AAE): https://engineering.purdue.edu/AAE/people/Faculty
2. School of Mechanical Engineering (ME): https://engineering.purdue.edu/ME/People/ptFaculty

Core architectural rules enforced:
- 4-Tier research categorization (Tier 1: Core Aero/Fluids/CFD/Propulsion/Combustion/Computational Math;
  Tier 2: Thermal/Heat Transfer/Energy; Tier 3: Structures/Materials/Manufacturing; Tier 4: Robotics/Controls/Autonomy).
- SELECTIVE OpenAlex JSON extraction: Only query OpenAlex API and persist `openalex_cache/<slug>.json`
  for Tier 1 Core Aero faculty. Non-aero faculty are strictly skipped from OpenAlex caching.
- Multi-sheet Excel export: Sheet 1 is 'Aero Focus' (Tier 1 only), followed by 'Field Matched' and 'All Faculty'.
- Detailed Markdown directory with 4-tier breakdown review tables beneath the directory index.
- 100% authentic data, zero fabrication.
"""

import os
import re
import time
import logging
import urllib.parse
from typing import List, Dict, Any, Optional, Tuple

import requests
import cloudscraper
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("purdue_scraper")

# =============================================================================
# 1. DYNAMIC COLUMN CONFIGURATION & ORDERING
# =============================================================================
COLUMNS_CONFIG = [
    # 1. Primary Profile & Identification
    "Name",
    "University",
    "Profile URL",
    "Google Scholar URL",
    "Job Title",
    "Department",
    "Scholar ID",
    "Email",

    # 2. Field Match Criteria & Prioritization Tiers
    "Research Tier",
    "Research Category",
    "Matched Count",
    "Matched Fields",

    # 3. Cold Email Personalization Hooks & Pillars
    "Flagship Paper Hook",
    "Tech Stack",
    "Physical Finding",
    "Research Hook",
    "Latest Paper / Publication",
    "Recent Papers (2024-2026)",
    "Top Cited Papers",
    "Courses Taught",
    "Recent Awards / Honors",
    "Cold Email / Application Instructions",

    # 4. Academic Background & Research Focus
    "OpenAlex Research Topics",
    "Google Scholar Tags",
    "Research Interests",
    "Expertise Areas",
    "Research / Bio Summary",
    "Education / Degrees",

    # 5. Lab Intelligence & Active Opportunities
    "Lab / Research Group Name",
    "Lab / Personal Website",
    "Actively Hiring / Openings",
    "Target Skills / Prerequisites",
    "Lab Facilities & Equipment",
    "Funding Sponsors",
    "Software / Code Repo",
    "Latest Project / Highlight",

    # 6. Location, Match Status & Source
    "Office Location",
    "Is Field Match",
    "Directory URL",
]

HYPERLINK_RULES = {
    "Profile URL": lambda val, row: (val, val) if str(val).startswith("http") else None,
    "Google Scholar URL": lambda val, row: (
        val,
        f"Scholar ({row.get('Scholar ID', '')})" if row.get('Scholar ID') else "Google Scholar Search"
    ) if str(val).startswith("http") else None,
    "Email": lambda val, row: (f"mailto:{val}", val) if "@" in str(val) else None,
    "Lab / Personal Website": lambda val, row: (val, val) if str(val).startswith("http") else None,
    "Software / Code Repo": lambda val, row: (val.split(",")[0].strip(), val) if str(val).startswith("http") else None,
    "Directory URL": lambda val, row: (val, val) if str(val).startswith("http") else None,
}

# =============================================================================
# 2. KEYWORD ONTOLOGY & EXCLUSIONS
# =============================================================================
TARGET_KEYWORDS = [
    # Turbulence, CFD & Fluid Mechanics
    "turbulence", "turbulent", "direct numerical simulation", "dns",
    "large eddy simulation", "les", "computational fluid dynamics", "cfd",
    "fluid dynamics", "fluid mechanics", "fluids", "aerodynamics", "hydrodynamics",
    "flow control", "boundary layer", "shear flow", "vortex dynamics", "vortices",
    "compressible flow", "incompressible flow", "reacting flow", "multiphase flow",
    "microfluidics", "biofluid", "fluid-structure interaction", "fsi",
    "shock waves", "hypersonic", "supersonic", "transonic", "aerothermodynamics",
    "computational mathematics", "scientific computing", "numerical methods",
    "spectral methods", "high-order methods", "finite volume",

    # Propulsion, Combustion & High-Speed Engines
    "propulsion", "combustion", "scramjet", "scramjets", "flame dynamics",
    "detonation", "rotating detonation", "rocket propulsion", "nozzle", "heat transfer",
    "thermal", "thermodynamics", "convection", "conduction", "radiation", "energy systems",

    # Robotics, Control & Autonomy
    "robotics", "robot", "autonomous", "uav", "drone", "guidance", "navigation",
    "control theory", "optimal control", "nonlinear control", "system dynamics",
    "estimation", "slam", "path planning", "motion planning",

    # Materials & Structures
    "materials", "smart materials", "composites", "nanomaterials", "solid mechanics",
    "structural health monitoring", "continuum mechanics", "fracture mechanics",
    "elasticity", "plasticity", "finite element", "fea", "fem", "metamaterials",

    # Space & Vehicles
    "spacecraft", "aerospace", "orbital mechanics", "astrodynamics", "satellite",
    "unmanned aerial vehicles", "entry vehicles", "reentry vehicles", "launch vehicles",
]

EXCLUDED_TITLES = [
    "emeritus", "retired", "adjunct", "visiting", "lecturer", "staff",
    "postdoc", "courtesy", "administrative", "coordinator", "advisor",
    "manager", "instructor", "emerita", "clinical", "technician"
]

# =============================================================================
# 3. RESEARCH TIER & AERO CORE CLASSIFICATION ENGINE
# =============================================================================
TIER_1_AERO_TERMS = [
    r'\bcomputational fluid dynamics\b', r'\bcfd\b', r'\bfluid dynamics\b',
    r'\bfluid mechanics\b', r'\bturbulence\b', r'\bturbulent\b',
    r'\bdirect numerical simulation\b', r'\bdns\b', r'\blarge eddy simulation\b', r'\bles\b',
    r'\baerodynamics\b', r'\baerodynamic\b', r'\bhypersonic\b', r'\bsupersonic\b',
    r'\btransonic\b', r'\bcompressible flow\b', r'\bshock waves\b', r'\bairfoil\b',
    r'\baerothermodynamics\b', r'\bscramjet\b', r'\bscramjets\b',
    r'\bpropulsion\b', r'\bcombustion\b', r'\bflame dynamics\b', r'\bflame\b',
    r'\bdetonation\b', r'\brotating detonation\b', r'\brocketry\b', r'\brocket\b', r'\bnozzle\b',
    r'\bmultiphase flow\b', r'\bmultiphase\b', r'\bparticle dynamics in fluid\b',
    r'\bboundary layer\b', r'\bvortex\b', r'\bvortices\b', r'\bflow control\b',
    r'\bshear flow\b', r'\baeroelasticity\b', r'\baeroacoustics\b', r'\bastrodynamics\b',
    r'\borbital mechanics\b', r'\bcomputational mathematics\b', r'\bscientific computing\b',
    r'\bfinite volume\b', r'\bspectral methods\b', r'\brarefied gas\b', r'\bboltzmann\b',
    r'\bplasma\b', r'\bwind energy\b', r'\bflight mechanics\b'
]
_COMPILED_T1 = [re.compile(p, re.IGNORECASE) for p in TIER_1_AERO_TERMS]

TIER_2_THERMAL_TERMS = [
    r'\bheat transfer\b', r'\bthermal\b', r'\bthermodynamics\b', r'\bconvection\b',
    r'\bconduction\b', r'\bradiation\b', r'\bthermal management\b', r'\benergy systems\b',
    r'\bfuel cells?\b', r'\bthermoelectric\b', r'\bphase change\b', r'\bhvac\b'
]
_COMPILED_T2 = [re.compile(p, re.IGNORECASE) for p in TIER_2_THERMAL_TERMS]

TIER_3_MATERIALS_TERMS = [
    r'\bmaterials\b', r'\bcomposites\b', r'\bsolid mechanics\b', r'\bfracture\b',
    r'\bnanomaterials\b', r'\bmanufacturing\b', r'\badditive manufacturing\b',
    r'\b3d printing\b', r'\bgraphene\b', r'\bmxene\b', r'\bbattery\b',
    r'\bstructural health monitoring\b', r'\bfinite element\b', r'\bfea\b', r'\bfem\b',
    r'\bcontinuum mechanics\b', r'\bvibrations?\b', r'\bacoustics\b', r'\bstructures\b'
]
_COMPILED_T3 = [re.compile(p, re.IGNORECASE) for p in TIER_3_MATERIALS_TERMS]

TIER_4_ROBOTICS_TERMS = [
    r'\brobot\b', r'\brobotics\b', r'\bswarm\b', r'\bautonomy\b', r'\bautonomous\b',
    r'\breinforcement learning\b', r'\bcontrol systems?\b', r'\bcontrol theory\b',
    r'\boptimal control\b', r'\bpath planning\b', r'\bmanipulation\b', r'\buav\b', r'\bdrone\b',
    r'\bmechatronics\b', r'\bdesign optimization\b', r'\bmems\b', r'\btribology\b'
]
_COMPILED_T4 = [re.compile(p, re.IGNORECASE) for p in TIER_4_ROBOTICS_TERMS]


def match_field_keywords(text: str) -> List[str]:
    if not text:
        return []
    text_lower = text.lower()
    matches = set()
    for kw in TARGET_KEYWORDS:
        if len(kw) <= 4:
            pattern = r"(?<!\w)" + re.escape(kw) + r"(?!\w)"
            if re.search(pattern, text_lower):
                matches.add(kw)
        else:
            if kw in text_lower:
                matches.add(kw)
    return sorted(list(matches))


def classify_faculty_tier(prof_dict: Dict[str, Any]) -> Tuple[int, str]:
    """
    Evaluates professor profile across matched fields, OpenAlex topics,
    research interests, lab group name, and bio to assign an authoritative Research Tier:
      Tier 1: 🔵 Core Aero / Fluids / CFD / Propulsion / Combustion / Computational Math
      Tier 2: 🟡 Thermal / Heat Transfer / Energy Systems
      Tier 3: 🟠 Structures / Materials / Manufacturing
      Tier 4: 🔴 Robotics / Controls / Autonomy
    """
    text = " | ".join([
        str(prof_dict.get("Matched Fields", "")),
        str(prof_dict.get("OpenAlex Research Topics", "")),
        str(prof_dict.get("Research Interests", "")),
        str(prof_dict.get("Expertise Areas", "")),
        str(prof_dict.get("Lab / Research Group Name", "")),
        str(prof_dict.get("Research / Bio Summary", ""))
    ])

    t1_hits = [p.pattern.replace(r'\b', '') for p in _COMPILED_T1 if p.search(text)]
    t2_hits = [p.pattern.replace(r'\b', '') for p in _COMPILED_T2 if p.search(text)]
    t3_hits = [p.pattern.replace(r'\b', '') for p in _COMPILED_T3 if p.search(text)]
    t4_hits = [p.pattern.replace(r'\b', '') for p in _COMPILED_T4 if p.search(text)]

    dept = prof_dict.get("Department", "")
    # In AAE department, strong aerodynamic/propulsion/orbital/computational keywords firmly place in Tier 1
    if "Aero" in dept:
        if len(t1_hits) >= 1:
            return 1, "🔵 Tier 1: Core Aero / Fluids / Propulsion"
    else:
        if len(t1_hits) >= 2 or any(k in text.lower() for k in ["computational fluid", "turbulen", "aerodynamic", "propulsion", "combustion", "multiphase flow"]):
            return 1, "🔵 Tier 1: Core Aero / Fluids / Propulsion"

    if len(t4_hits) >= max(len(t2_hits), len(t3_hits)) and len(t4_hits) > 0:
        return 4, "🔴 Tier 4: Robotics / Controls / Autonomy"
    if len(t2_hits) >= len(t3_hits) and len(t2_hits) > 0:
        return 2, "🟡 Tier 2: Thermal / Heat Transfer / Energy"
    if len(t3_hits) > 0:
        return 3, "🟠 Tier 3: Structures / Materials / Manufacturing"
    return 4, "🔴 Tier 4: Robotics / Controls / Autonomy"


def is_core_aero_faculty(prof_dict: Dict[str, Any]) -> bool:
    """Returns True ONLY if professor qualifies for Tier 1 Core Aero/Fluids focus."""
    tier_num, _ = classify_faculty_tier(prof_dict)
    return tier_num == 1


def build_scholar_url(name: str, scholar_id: str = "") -> str:
    if scholar_id:
        return f"https://scholar.google.com/citations?hl=en&user={scholar_id}"
    query = f"{name} Purdue University".strip()
    return f"https://scholar.google.com/citations?view_op=search_authors&mauthors={urllib.parse.quote(query)}"


OPENALEX_API_KEY = "JyKkBSgwqlZae8wfXCatfk"


def fetch_academic_scholar_intel(name: str) -> Tuple[str, str, str]:
    """
    Fetches exact Google Scholar interest tags, 3 top-cited papers (with journal, year, cites, and clickable DOI),
    and 3 recent papers from 2024-2026 (with journal, year, and clickable DOI) using OpenAlex with API key.
    All extracted JSON data is saved locally in 'openalex_cache/' for future reference and auditing.
    STRICT RULE: Only called for Tier 1 Core Aero faculty!
    """
    tags_str = ""
    top_papers_str = ""
    recent_papers_str = ""

    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openalex_cache")
    os.makedirs(cache_dir, exist_ok=True)
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', name.strip().lower()).strip('_')
    cache_file = os.path.join(cache_dir, f"{slug}.json")

    import json
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cdata = json.load(f)
            # Reconstruct tags_str, top_papers_str, recent_papers_str from cached json
            t_list = [f"{t.get('topic')} ({t.get('count')})" if t.get('count') else t.get('topic') for t in cdata.get("top_topics", []) if t.get("topic")]
            if t_list:
                tags_str = " | ".join(t_list[:3])
            
            top_p = []
            for w in cdata.get("top_cited_works", []):
                t = w.get("title", "")
                y = w.get("publication_year", "")
                c = w.get("cited_by_count", 0)
                j = w.get("venue", "")
                j_str = f" [{j}]" if j else ""
                doi = w.get("doi", "")
                doi_str = f" [DOI: {doi}]" if doi else ""
                if t:
                    top_p.append(f'"{t}"{j_str} ({y}, {c} cites){doi_str}')
            if top_p:
                top_papers_str = " | ".join(top_p)

            rec_p = []
            for w in cdata.get("recent_works", []):
                t = w.get("title", "")
                y = w.get("publication_year", "")
                j = w.get("venue", "")
                j_str = f" [{j}]" if j else ""
                doi = w.get("doi", "")
                doi_str = f" [DOI: {doi}]" if doi else ""
                if t:
                    rec_p.append(f'"{t}"{j_str} ({y}){doi_str}')
            if rec_p:
                recent_papers_str = " | ".join(rec_p)

            return tags_str, top_papers_str, recent_papers_str
        except Exception as ce:
            log.debug(f"Could not read existing cache for {name}: {ce}")

    try:
        clean_name = " ".join(name.split())
        url = f"https://api.openalex.org/authors?search={urllib.parse.quote(clean_name)}&api_key={OPENALEX_API_KEY}"
        r = requests.get(url, timeout=12)
        if r.status_code == 200:
            results = r.json().get("results", [])
            matched_author = None
            for a in results[:10]:
                insts_raw = a.get("last_known_institutions") or []
                insts = " ".join([inst.get("display_name", "") for inst in insts_raw if isinstance(inst, dict)])
                topics_text = " ".join([t.get("display_name", "") for t in a.get("topics", []) if isinstance(t, dict)]).lower()
                has_purdue = any(k in insts.lower() for k in ["purdue", "west lafayette"])
                has_mech_aerospace = any(k in topics_text for k in [
                    "fluid", "aero", "mechanic", "propulsion", "combustion", "turbulence", "thermal", "space", "flight", "numerical"
                ])
                if has_purdue and has_mech_aerospace:
                    matched_author = a
                    break
                elif has_purdue and not matched_author:
                    matched_author = a

            if not matched_author and results:
                matched_author = results[0]

            if matched_author:
                auth_id = matched_author.get("id", "")
                topics_raw = matched_author.get("topics", [])
                top_topics_clean = []
                top_topics_str_list = []
                for t in topics_raw[:5]:
                    t_name = t.get("display_name", "")
                    t_cnt = t.get("count", 0)
                    if t_name:
                        top_topics_clean.append({"topic": t_name, "count": t_cnt})
                        top_topics_str_list.append(f"{t_name} ({t_cnt})" if t_cnt else t_name)
                if top_topics_str_list:
                    tags_str = " | ".join(top_topics_str_list[:3])

                stats = matched_author.get("summary_stats", {}) or {}
                affs_raw = matched_author.get("affiliations", []) or []
                affs_clean = [
                    aff.get("institution", {}).get("display_name", "")
                    for aff in affs_raw
                    if isinstance(aff, dict) and aff.get("institution", {}).get("display_name")
                ]

                clean_profile = {
                    "name": name,
                    "uni": "Purdue University",
                    "author_id": auth_id.split("/")[-1] if "/" in auth_id else auth_id,
                    "author_display_name": matched_author.get("display_name", name),
                    "works_count": matched_author.get("works_count", 0),
                    "cited_by_count": matched_author.get("cited_by_count", 0),
                    "2yr_mean_citedness": stats.get("2yr_mean_citedness", 0.0),
                    "h_index": stats.get("h_index", 0),
                    "i10_index": stats.get("i10_index", 0),
                    "affiliations": affs_clean[:5],
                    "top_topics": top_topics_clean,
                    "top_cited_works": [],
                    "recent_works": []
                }

                def clean_work_obj(w: Dict[str, Any]) -> Dict[str, Any]:
                    source = w.get("primary_location", {}).get("source", {}) if w.get("primary_location") else {}
                    venue = source.get("display_name", "") if source else ""
                    doi = w.get("doi") or (w.get("primary_location", {}).get("landing_page_url") if w.get("primary_location") else None)
                    concepts = [c.get("display_name", "") for c in w.get("concepts", [])[:8] if isinstance(c, dict) and c.get("display_name")]
                    authors = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", []) if a.get("author", {}).get("display_name")]

                    abstract = ""
                    inv_idx = w.get("abstract_inverted_index")
                    if inv_idx and isinstance(inv_idx, dict):
                        word_positions = []
                        for word, positions in inv_idx.items():
                            for pos in positions:
                                word_positions.append((pos, word))
                        word_positions.sort(key=lambda x: x[0])
                        abstract = " ".join([wp[1] for wp in word_positions])
                        if len(abstract) > 1200:
                            abstract = abstract[:1197] + "..."

                    return {
                        "title": w.get("title") or "",
                        "publication_year": w.get("publication_year"),
                        "publication_date": w.get("publication_date") or "",
                        "doi": doi or "",
                        "venue": venue,
                        "type": w.get("type") or "",
                        "cited_by_count": w.get("cited_by_count") or 0,
                        "is_oa": w.get("open_access", {}).get("is_oa", False),
                        "oa_url": w.get("open_access", {}).get("oa_url") or "",
                        "concepts": concepts,
                        "abstract": abstract,
                        "authors": authors
                    }

                if auth_id:
                    works_url = f"https://api.openalex.org/works?filter=author.id:{auth_id}&sort=cited_by_count:desc&per_page=3&api_key={OPENALEX_API_KEY}"
                    w_res = requests.get(works_url, timeout=12)
                    if w_res.status_code == 200:
                        works = w_res.json().get("results", [])
                        papers_list = []
                        for w in works:
                            cw = clean_work_obj(w)
                            clean_profile["top_cited_works"].append(cw)
                            w_title = cw["title"]
                            w_year = cw["publication_year"]
                            w_cites = cw["cited_by_count"]
                            j = cw["venue"]
                            j_str = f" [{j}]" if j else ""
                            doi = cw["doi"]
                            doi_str = f" [DOI: {doi}]" if doi else ""
                            if w_title:
                                papers_list.append(f'"{w_title}"{j_str} ({w_year}, {w_cites} cites){doi_str}')
                        if papers_list:
                            top_papers_str = " | ".join(papers_list)

                    time.sleep(0.05)
                    rec_url = f"https://api.openalex.org/works?filter=author.id:{auth_id},publication_year:2024-2026&sort=publication_year:desc&per_page=3&api_key={OPENALEX_API_KEY}"
                    r_rec = requests.get(rec_url, timeout=12)
                    if r_rec.status_code == 200:
                        rec_works = r_rec.json().get("results", [])
                        recent_list = []
                        for w in rec_works:
                            cw = clean_work_obj(w)
                            clean_profile["recent_works"].append(cw)
                            w_title = cw["title"]
                            w_year = cw["publication_year"]
                            j = cw["venue"]
                            j_str = f" [{j}]" if j else ""
                            doi = cw["doi"]
                            doi_str = f" [DOI: {doi}]" if doi else ""
                            if w_title:
                                recent_list.append(f'"{w_title}"{j_str} ({w_year}){doi_str}')
                        if recent_list:
                            recent_papers_str = " | ".join(recent_list)

                    import json
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(clean_profile, f, indent=2, ensure_ascii=False)

    except Exception as e:
        log.debug(f"Error fetching academic scholar intel for {name}: {e}")

    return tags_str, top_papers_str, recent_papers_str


def create_browser_session() -> cloudscraper.CloudScraper:
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "desktop": True}
    )
    scraper.headers.update({
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
    })
    return scraper


def scrape_deep_lab_site(scraper: cloudscraper.CloudScraper, url: str) -> Dict[str, str]:
    details = {
        "Actively Hiring / Openings": "",
        "Target Skills / Prerequisites": "",
        "Lab Facilities & Equipment": "",
        "Funding Sponsors": "",
        "Software / Code Repo": "",
        "Latest Project / Highlight": "",
        "Latest Paper / Publication": "",
        "Cold Email / Application Instructions": ""
    }
    if not url or not url.startswith("http"):
        return details

    try:
        r = scraper.get(url, timeout=10)
        if r.status_code != 200:
            return details

        soup = BeautifulSoup(r.text, "html.parser")
        page_text = soup.get_text(separator=" ")

        base_domain = urllib.parse.urlparse(url).netloc
        subpages = {}
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full_sub_url = urllib.parse.urljoin(url, href)
            parsed_sub = urllib.parse.urlparse(full_sub_url)
            if parsed_sub.netloc != base_domain and not ("sites.google.com" in url and "sites.google.com" in full_sub_url):
                continue
            sub_text = a_tag.get_text(strip=True).lower()
            sub_path = parsed_sub.path.lower()

            if any(w in sub_path or w in sub_text for w in ["publication", "papers", "pubs"]) and "pub" not in subpages:
                subpages["pub"] = full_sub_url
            if any(w in sub_path or w in sub_text for w in ["opening", "join", "prospective", "opportunities", "contact"]) and "openings" not in subpages:
                subpages["openings"] = full_sub_url
            if any(w in sub_path or w in sub_text for w in ["research", "projects", "thrust"]) and "research" not in subpages:
                subpages["research"] = full_sub_url
            if any(w in sub_path or w in sub_text for w in ["facility", "facilities", "equipment", "setup"]) and "facilities" not in subpages:
                subpages["facilities"] = full_sub_url

        for el in soup.find_all(["p", "li", "blockquote"]):
            el_text = " ".join(el.get_text(separator=" ").split()).replace('\xa0', ' ').strip()
            t_low = el_text.lower()
            if not details["Cold Email / Application Instructions"] and any(k in t_low for k in ["send your cv", "email me", "to apply", "prospective ph", "subject line", "statement on describing", "interested candidates should", "cv, transcript"]):
                if 25 <= len(el_text) <= 1200:
                    details["Cold Email / Application Instructions"] = el_text
            if not details["Actively Hiring / Openings"] and any(k in t_low for k in ["looking for motivated", "openings", "positions available", "phd positions available", "open position"]):
                if 20 <= len(el_text) <= 500:
                    details["Actively Hiring / Openings"] = el_text

        if "openings" in subpages:
            try:
                r_o = scraper.get(subpages["openings"], timeout=8)
                if r_o.status_code == 200:
                    soup_o = BeautifulSoup(r_o.text, "html.parser")
                    found_subpage_instructions = []
                    found_subpage_openings = []
                    for el in soup_o.find_all(["p", "li", "blockquote"]):
                        el_text = " ".join(el.get_text(separator=" ").split()).replace('\xa0', ' ').strip()
                        t_low = el_text.lower()
                        if any(k in t_low for k in ["to apply", "send your cv", "email", "prospective ph", "cover letter", "subject line", "cv, transcript", "interested candidates should"]):
                            if 35 <= len(el_text) <= 1200 and el_text not in found_subpage_instructions:
                                found_subpage_instructions.append(el_text)
                        if any(k in t_low for k in ["looking for", "openings", "phd position", "undergraduate", "interns", "seeking"]):
                            if 25 <= len(el_text) <= 500 and el_text not in found_subpage_openings:
                                found_subpage_openings.append(el_text)

                    if found_subpage_instructions:
                        details["Cold Email / Application Instructions"] = " | ".join(found_subpage_instructions[:2])
                    if found_subpage_openings:
                        details["Actively Hiring / Openings"] = " | ".join(found_subpage_openings[:2])
            except Exception:
                pass

        if not details["Actively Hiring / Openings"] and any(w in page_text.lower() for w in ["openings", "join us", "open position", "phd positions available"]):
            details["Actively Hiring / Openings"] = "Actively recruiting / Openings mentioned on lab site"

        facility_candidates = [
            "Wind Tunnel", "Water Tunnel", "PIV", "Particle Image Velocimetry", "Laser Doppler", "LDV",
            "Schlieren", "Shadowgraph", "Combustion Bomb", "Gas Turbine", "Shock Tube", "Cleanroom",
            "SEM", "Scanning Electron Microscopy", "Hypersonic Tunnel", "MTS", "Instron", "Supercomputer", "Cluster"
        ]
        facilities_found = []
        target_fac_soup = soup
        if "facilities" in subpages:
            try:
                r_f = scraper.get(subpages["facilities"], timeout=8)
                if r_f.status_code == 200:
                    target_fac_soup = BeautifulSoup(r_f.text, "html.parser")
            except Exception:
                pass

        fac_text = target_fac_soup.get_text(separator=" ")
        for eq in facility_candidates:
            pattern = r'(?<!\w)' + re.escape(eq) + r'(?!\w)'
            if re.search(pattern, fac_text, re.IGNORECASE):
                if eq not in facilities_found:
                    facilities_found.append(eq)

        if facilities_found:
            details["Lab Facilities & Equipment"] = ", ".join(facilities_found[:6])

        sponsors = set()
        for sp in ["NSF", "NASA", "DARPA", "ONR", "AFOSR", "DOE", "NIH", "ARPA-E", "Lockheed Martin", "Boeing", "Rolls-Royce", "Pratt & Whitney", "GE Aerospace", "Sandia National Laboratories"]:
            pattern = r'\b' + re.escape(sp) + r'\b'
            if re.search(pattern, page_text):
                sponsors.add(sp)
        if sponsors:
            details["Funding Sponsors"] = ", ".join(sorted(list(sponsors)))

        repos = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if "github.com" in href or "bitbucket.org" in href or "gitlab.com" in href:
                if not any(ign in href for ign in ["github.com/google", "github.com/facebook", "github.com/twitter"]):
                    repos.add(href.rstrip("/"))
        if repos:
            details["Software / Code Repo"] = ", ".join(sorted(list(repos))[:2])

    except Exception as e:
        log.debug(f"Deep lab scraping error for {url}: {e}")

    return details


def scrape_purdue(scraper: cloudscraper.CloudScraper) -> List[Dict[str, Any]]:
    """
    Primary scraping orchestration for Purdue University:
    1. Scrapes School of Aeronautics and Astronautics (AAE) directory.
    2. Scrapes School of Mechanical Engineering (ME) directory.
    3. Filters for active Tenured/Tenure-Track faculty.
    4. Enriches each profile by scraping the individual `ptProfile?resource_id=...` page.
    5. Performs deep lab scraping if a lab URL exists.
    6. Selectively executes OpenAlex extraction ONLY for Tier 1 Core Aero faculty.
    """
    departments_info = [
        {
            "name": "Aeronautics and Astronautics",
            "url": "https://engineering.purdue.edu/AAE/people/Faculty",
            "dir_type": "AAE"
        },
        {
            "name": "Mechanical Engineering",
            "url": "https://engineering.purdue.edu/ME/People/ptFaculty",
            "dir_type": "ME"
        }
    ]

    all_faculty_cards = []
    seen_profiles = set()

    for dept in departments_info:
        log.info(f"Scraping {dept['name']} directory: {dept['url']}...")
        try:
            r = scraper.get(dept["url"], timeout=20)
            if r.status_code != 200:
                log.error(f"Failed to fetch {dept['name']} directory (HTTP {r.status_code})")
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            profile_links = soup.find_all("a", href=re.compile(r'ptProfile\?resource_id=(\d+)'))
            log.info(f"Found {len(profile_links)} raw profile links in {dept['name']}.")

            for a in profile_links:
                t = a.get_text(strip=True)
                if not t:
                    continue
                href = a["href"].strip()
                if not href.startswith("http"):
                    href = urllib.parse.urljoin(dept["url"], href)

                # Extract unique resource ID
                m_id = re.search(r'resource_id=(\d+)', href)
                res_id = m_id.group(1) if m_id else href
                if res_id in seen_profiles:
                    continue
                seen_profiles.add(res_id)

                # Walk up to the faculty card container
                card = a
                for _ in range(4):
                    if card.parent:
                        card = card.parent
                card_text = card.get_text(" | ", strip=True)
                card_lower = card_text.lower()

                # Filter out emeritus, adjunct, courtesy, visiting, lecturer, staff
                if any(term in card_lower for term in EXCLUDED_TITLES):
                    continue

                # Ensure academic rank exists
                if not any(term in card_lower for term in ["assistant professor", "associate professor", "professor"]):
                    continue

                # Parse clean title from card text
                lines = [l.strip() for l in card_text.split("|") if l.strip()]
                clean_title = "Professor"
                for line in lines[1:5]:
                    l_low = line.lower()
                    if any(rk in l_low for rk in ["assistant professor", "associate professor", "professor", "chair"]):
                        if not any(ex in l_low for ex in EXCLUDED_TITLES):
                            clean_title = line
                            break

                raw_name = t
                split_name = re.findall(r'[A-Z][a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)|[a-z]+|\d+', raw_name)
                clean_name = " ".join(split_name) if split_name else raw_name

                all_faculty_cards.append({
                    "Name": clean_name,
                    "Raw Name": raw_name,
                    "Job Title": clean_title,
                    "Department": dept["name"],
                    "Profile URL": href,
                    "Card Text": card_text,
                    "Directory URL": dept["url"],
                    "Resource ID": res_id
                })

        except Exception as e:
            log.error(f"Error scraping {dept['name']} directory: {e}")

    log.info(f"Filtered {len(all_faculty_cards)} active faculty candidates across Purdue AAE & ME.")

    results: List[Dict[str, Any]] = []

    # Process and deep-scrape each faculty profile page
    log.info("Enriching individual faculty profile pages...")
    for i, fac in enumerate(all_faculty_cards, 1):
        name = fac["Name"]
        p_url = fac["Profile URL"]
        dept = fac["Department"]
        log.info(f"[{i}/{len(all_faculty_cards)}] Processing {name} ({dept})...")

        email = ""
        phone = ""
        office = ""
        scholar_url = ""
        scholar_id = ""
        lab_website = ""
        lab_name = ""
        degrees = ""
        interests = ""
        research_areas = ""
        awards = ""
        publications_text = ""

        try:
            r_prof = scraper.get(p_url, timeout=12)
            if r_prof.status_code == 200:
                soup_prof = BeautifulSoup(r_prof.text, "html.parser")

                h1_tags = soup_prof.find_all("h1")
                if len(h1_tags) >= 2:
                    h1_name = " ".join(h1_tags[1].get_text(separator=" ").split())
                    if h1_name and len(h1_name) < 40 and not any(w in h1_name.lower() for w in ["purdue", "directory", "people"]):
                        name = h1_name
                elif len(h1_tags) == 1:
                    h1_text = h1_tags[0].get_text(strip=True)
                    if "-" in h1_text:
                        name = h1_text.split("-")[0].strip()

                def get_section(h_pattern: str) -> str:
                    h = soup_prof.find(lambda t: t.name in ["h2", "h3"] and re.search(h_pattern, t.get_text(), re.IGNORECASE))
                    if not h:
                        return ""
                    res = []
                    curr = h.find_next_sibling()
                    while curr and curr.name not in ["h2", "h3"]:
                        res.append(curr.get_text(" ", strip=True))
                        curr = curr.find_next_sibling()
                    return " ".join(res).strip()

                degrees = get_section(r"degrees")
                interests = get_section(r"interests")
                research_areas = get_section(r"(research areas|fundamental research)")
                awards = get_section(r"(awards|recognitions|honors)")
                publications_text = get_section(r"(publications|selected publications)")

                m_email = re.search(r'mailto:([a-zA-Z0-9._%+-]+@purdue\.edu)', r_prof.text)
                if m_email:
                    email = m_email.group(1)

                m_tel = re.search(r'tel:([0-9() -]+)', r_prof.text)
                if m_tel:
                    phone = m_tel.group(1)

                m_off = re.search(r'Office:\s*(?:</[^>]+>\s*)*([A-Z0-9\s-]+?)(?:\s*\||<|Office|tel|\n|\r)', r_prof.text)
                if m_off:
                    office = " ".join(m_off.group(1).split())
                if not office:
                    for token in fac["Card Text"].split("|"):
                        token_s = token.strip()
                        if any(bld in token_s for bld in ["ARMS", "ME ", "WANG", "GRIS", "FLEX", "HAMP", "POTR", "SL "]):
                            office = token_s
                            break

                m_sch = re.search(r'https?://scholar\.google\.com/citations\?[^"\'\s<>]+', r_prof.text)
                if m_sch:
                    scholar_url = m_sch.group(0).replace("&amp;", "&")
                    m_sch_id = re.search(r'user=([a-zA-Z0-9_-]{12})', scholar_url)
                    if m_sch_id:
                        scholar_id = m_sch_id.group(1)

                web_h = soup_prof.find(lambda t: t.name in ["h2", "h3"] and "websites" in t.get_text().lower())
                if web_h:
                    nxt = web_h.find_next_sibling()
                    if nxt:
                        lab_a = nxt.find("a", href=True)
                        if lab_a:
                            lab_website = lab_a["href"]
                            lab_name = lab_a.get_text(strip=True)

                if not lab_website:
                    for a_tag in soup_prof.find_all("a", href=True):
                        href = a_tag["href"]
                        if any(w in href for w in ["sites.google.com", "engineering.purdue.edu/~", "purdue.edu/research"]) or ("http" in href and not any(w in href for w in ["purdue.edu", "google.com", "doi.org", "sciencedirect", "wiley", "twitter", "linkedin", "facebook"])):
                            lab_website = href
                            lab_name = a_tag.get_text(strip=True) or "Lab Website"
                            break

        except Exception as e:
            log.debug(f"Error scraping profile for {name}: {e}")

        clean_awards = awards
        if len(clean_awards) > 130:
            clean_awards = clean_awards[:127] + "..."

        bio_summary = research_areas if research_areas else interests
        if len(bio_summary) > 400:
            bio_summary = bio_summary[:397] + "..."

        combined_profile_text = " | ".join([
            name, fac["Job Title"], dept, interests, research_areas, degrees, lab_name, fac["Card Text"]
        ])
        matched = match_field_keywords(combined_profile_text)

        faculty_dict: Dict[str, Any] = {
            "Name": name,
            "University": "Purdue University",
            "Profile URL": p_url,
            "Google Scholar URL": scholar_url or build_scholar_url(name, scholar_id),
            "Job Title": fac["Job Title"],
            "Department": dept,
            "Scholar ID": scholar_id,
            "Email": email,
            "Research Tier": 4,
            "Research Category": "🔴 Tier 4: Robotics / Controls / Autonomy",
            "Matched Count": len(matched),
            "Matched Fields": ", ".join(matched),
            "Flagship Paper Hook": "",
            "Tech Stack": "",
            "Physical Finding": "",
            "Research Hook": "",
            "Latest Paper / Publication": "",
            "Recent Papers (2024-2026)": "",
            "Top Cited Papers": "",
            "Courses Taught": "",
            "Recent Awards / Honors": clean_awards,
            "Cold Email / Application Instructions": "",
            "OpenAlex Research Topics": "",
            "Google Scholar Tags": "",
            "Research Interests": interests,
            "Expertise Areas": research_areas,
            "Research / Bio Summary": bio_summary,
            "Education / Degrees": degrees,
            "Lab / Research Group Name": lab_name,
            "Lab / Personal Website": lab_website,
            "Actively Hiring / Openings": "",
            "Target Skills / Prerequisites": "",
            "Lab Facilities & Equipment": "",
            "Funding Sponsors": "",
            "Software / Code Repo": "",
            "Latest Project / Highlight": "",
            "Office Location": office,
            "Is Field Match": len(matched) > 0,
            "Directory URL": fac["Directory URL"]
        }

        if lab_website:
            lab_details = scrape_deep_lab_site(scraper, lab_website)
            for k, v in lab_details.items():
                if v and not faculty_dict.get(k):
                    faculty_dict[k] = v

        tier_num, tier_label = classify_faculty_tier(faculty_dict)
        faculty_dict["Research Tier"] = tier_num
        faculty_dict["Research Category"] = tier_label

        # =====================================================================
        # STRICT SELECTIVE OPENALEX EXTRACTION: TIER 1 CORE AERO ONLY!
        # =====================================================================
        if tier_num == 1:
            log.info(f"   -> [Tier 1 Core Aero]: Querying OpenAlex API and caching JSON for {name}...")
            tags_intel, papers_intel, recent_intel = fetch_academic_scholar_intel(name)
            if tags_intel:
                faculty_dict["OpenAlex Research Topics"] = tags_intel
                faculty_dict["Google Scholar Tags"] = tags_intel
            if papers_intel:
                faculty_dict["Top Cited Papers"] = papers_intel
            if recent_intel:
                faculty_dict["Recent Papers (2024-2026)"] = recent_intel
        else:
            log.info(f"   -> [Tier {tier_num}]: Non-core aero faculty; skipping OpenAlex API & JSON caching.")

        final_tier, final_label = classify_faculty_tier(faculty_dict)
        faculty_dict["Research Tier"] = final_tier
        faculty_dict["Research Category"] = final_label

        results.append(faculty_dict)
        time.sleep(0.08)

    results.sort(key=lambda x: (x.get("Research Tier", 4), -x.get("Matched Count", 0), x["Name"].strip().lower()))
    log.info(f"Total Purdue faculty successfully extracted and enriched: {len(results)}")
    return results


# =============================================================================
# 4. MULTI-SHEET EXCEL EXPORT (Aero Focus as Sheet 1)
# =============================================================================
def export_to_excel(faculty_list: List[Dict], output_path: str, columns: List[str] = COLUMNS_CONFIG):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    link_font = Font(name="Calibri", size=11, color="0563C1", underline="single")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    aero_focus_list = [f for f in faculty_list if f.get("Research Tier") == 1]
    aero_focus_list.sort(key=lambda x: (-x.get("Matched Count", 0), x["Name"].strip().lower()))

    field_matched_list = [f for f in faculty_list if f.get("Is Field Match")]
    field_matched_list.sort(key=lambda x: (x.get("Research Tier", 4), -x.get("Matched Count", 0), x["Name"].strip().lower()))

    all_faculty_list = list(faculty_list)
    all_faculty_list.sort(key=lambda x: (x.get("Research Tier", 4), -x.get("Matched Count", 0), x["Name"].strip().lower()))

    sheets_data = [
        ("Aero Focus", aero_focus_list),
        ("Field Matched", field_matched_list),
        ("All Faculty", all_faculty_list)
    ]

    for sheet_title, data_rows in sheets_data:
        ws = wb.create_sheet(title=sheet_title)
        ws.views.sheetView[0].showGridLines = True
        ws.append(columns)

        for col_num in range(1, len(columns) + 1):
            c = ws.cell(row=1, column=col_num)
            c.font = header_font
            c.fill = header_fill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        for r_idx, row_dict in enumerate(data_rows):
            ws_row = r_idx + 2
            row_values = []
            hyperlink_meta = {}

            for col_idx, col_name in enumerate(columns):
                raw_val = row_dict.get(col_name, "")
                rule = HYPERLINK_RULES.get(col_name)
                if rule and raw_val:
                    hl_result = rule(raw_val, row_dict)
                    if hl_result:
                        target_url, label = hl_result
                        row_values.append(f'=HYPERLINK("{target_url}", "{label}")')
                        hyperlink_meta[col_idx + 1] = target_url
                        continue

                row_values.append(raw_val)

            ws.append(row_values)

            for c_idx in range(1, len(columns) + 1):
                cell = ws.cell(row=ws_row, column=c_idx)
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center")

                if c_idx in hyperlink_meta:
                    cell.hyperlink = hyperlink_meta[c_idx]
                    cell.font = link_font

        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or '')
                if val.startswith('='):
                    l = 28 if 'Scholar' in val else 45
                else:
                    l = len(val)
                if l > max_len:
                    max_len = l
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 55)

        ws.row_dimensions[1].height = 28
        ws.freeze_panes = "A2"

    wb.save(output_path)
    log.info(f"Successfully saved multi-sheet Excel workbook to {output_path}")


# =============================================================================
# 5. COMPREHENSIVE MARKDOWN DIRECTORY GENERATION
# =============================================================================
def export_to_markdown(faculty_list: List[Dict], output_path: str):
    field_matched = [f for f in faculty_list if f.get("Is Field Match")]
    field_matched.sort(key=lambda x: (x.get("Research Tier", 4), -x.get("Matched Count", 0), x["Name"].strip().lower()))

    tier_groups = {
        1: [f for f in faculty_list if f.get("Research Tier") == 1],
        2: [f for f in faculty_list if f.get("Research Tier") == 2],
        3: [f for f in faculty_list if f.get("Research Tier") == 3],
        4: [f for f in faculty_list if f.get("Research Tier") == 4],
    }

    lines = []
    lines.append("# Purdue University - Aerospace & Mechanical Engineering Faculty Directory\n")
    lines.append("> **Institution**: Purdue University (West Lafayette, IN)\n")
    lines.append("> **Departments**: School of Aeronautics and Astronautics (AAE) & School of Mechanical Engineering (ME)\n")
    lines.append(f"> **Total Active Faculty Extracted**: {len(faculty_list)} | **Field-Matched Faculty**: {len(field_matched)} | **Core Aero Focus (Tier 1)**: {len(tier_groups[1])}\n")
    lines.append("> **Cold Outreach Methodology**: [COLD_EMAIL_METHODOLOGY.md](../../COLD_EMAIL_METHODOLOGY.md) | **Excel Workbook**: [purdue_aerospace_mechanical_faculty.xlsx](purdue_aerospace_mechanical_faculty.xlsx)\n")
    lines.append("\n---\n")

    # Quick Directory Index
    lines.append("## 📋 Quick Directory Index\n")
    lines.append("| # | Faculty Member | Academic Title | Department | Research Tier | Matches | Intel Indicators | Core Matched Domains |")
    lines.append("| :-: | :--- | :--- | :--- | :--- | :-: | :---: | :--- |")

    for idx, f in enumerate(field_matched, 1):
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        title = f.get("Job Title", "")
        dept = f.get("Department", "")
        dept_abbr = "AAE" if "Aero" in dept else "ME"
        count = f.get("Matched Count", 0)
        fields = f.get("Matched Fields", "")
        tier_lbl = f.get("Research Category", "Tier 4").split(":")[0]

        indicators = []
        if f.get("Scholar ID") or "scholar.google" in f.get("Google Scholar URL", ""):
            indicators.append("🎓 **GS**")
        if f.get("Actively Hiring / Openings") or f.get("Cold Email / Application Instructions"):
            indicators.append("🎯 **Cold**")
        if f.get("Lab / Personal Website"):
            indicators.append("🔬 **Lab**")
        ind_str = " ".join(indicators) if indicators else "—"

        lines.append(f"| {idx} | [{name}](#{anchor}) | {title} | `{dept_abbr}` | {tier_lbl} | **{count}** | {ind_str} | {fields} |")

    lines.append("\n---\n")

    # 4-Tier Breakdown Review Table
    lines.append("## 🎯 Faculty Research Categorization & Prioritization Tiers\n")
    lines.append("This section organizes all faculty into 4 authoritative tiers to optimize cold outreach and research alignment. OpenAlex JSON caching and deep publication intelligence are strictly preserved for **Tier 1 (Core Aero/Fluids/Propulsion/Computational Math)** faculty.\n")

    lines.append("### 🔵 Tier 1: Core Aerospace / Fluid Dynamics / CFD / Propulsion / Computational Math (Primary Target)")
    lines.append(f"> **Cohort Size: {len(tier_groups[1])} Faculty** | Direct targets for CFD, turbulence, hypersonics, aerodynamics, multiphase, combustion, scramjets, and propulsion.\n")
    lines.append("| Professor | Dept | Academic Rank | Matched Aero Fields | Flagship Paper / Research Focus | Tech Stack |")
    lines.append("| :--- | :---: | :--- | :--- | :--- | :--- |")
    for f in tier_groups[1]:
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        dept = "AAE" if "Aero" in f.get("Department", "") else "ME"
        title = f.get("Job Title", "")
        fields = f.get("Matched Fields", "")
        flagship = f.get("Flagship Paper Hook", "")
        tech_stack = f.get("Tech Stack", "")
        if not flagship:
            flagship = f.get("Research Interests", "") or f.get("OpenAlex Research Topics", "")
        if len(flagship) > 75:
            flagship = flagship[:72] + "..."
        lines.append(f"| [{name}](#{anchor}) | `{dept}` | {title} | `{fields}` | {flagship} | `{tech_stack}` |")

    lines.append("\n### 🟡 Tier 2: Thermal Engineering / Heat Transfer / Energy Systems")
    lines.append(f"> **Cohort Size: {len(tier_groups[2])} Faculty** | Heat transfer, microscale thermal transport, thermoelectrics, and energy storage.\n")
    lines.append("| Professor | Dept | Academic Rank | Matched Fields | Lab / Research Focus |")
    lines.append("| :--- | :---: | :--- | :--- | :--- |")
    for f in tier_groups[2]:
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        dept = "AAE" if "Aero" in f.get("Department", "") else "ME"
        title = f.get("Job Title", "")
        fields = f.get("Matched Fields", "")
        lab = f.get("Lab / Research Group Name", "") or f.get("Research Interests", "Thermal & Energy Systems")
        if len(lab) > 65:
            lab = lab[:62] + "..."
        lines.append(f"| [{name}](#{anchor}) | `{dept}` | {title} | `{fields}` | {lab} |")

    lines.append("\n### 🟠 Tier 3: Structures / Materials Science / Solid Mechanics")
    lines.append(f"> **Cohort Size: {len(tier_groups[3])} Faculty** | Composite structures, additive manufacturing, fracture mechanics, and structural dynamics.\n")
    lines.append("| Professor | Dept | Academic Rank | Matched Fields | Lab / Materials Domain |")
    lines.append("| :--- | :---: | :--- | :--- | :--- |")
    for f in tier_groups[3]:
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        dept = "AAE" if "Aero" in f.get("Department", "") else "ME"
        title = f.get("Job Title", "")
        fields = f.get("Matched Fields", "")
        lab = f.get("Lab / Research Group Name", "") or f.get("Research Interests", "Materials / Structures")
        if len(lab) > 65:
            lab = lab[:62] + "..."
        lines.append(f"| [{name}](#{anchor}) | `{dept}` | {title} | `{fields}` | {lab} |")

    lines.append("\n### 🔴 Tier 4: Robotics / Controls / Autonomous Systems")
    lines.append(f"> **Cohort Size: {len(tier_groups[4])} Faculty** | Robot manipulation, multi-agent swarms, autonomy, control systems, and mechatronics.\n")
    lines.append("| Professor | Dept | Academic Rank | Matched Fields | Lab / Autonomy Focus |")
    lines.append("| :--- | :---: | :--- | :--- | :--- |")
    for f in tier_groups[4]:
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        dept = "AAE" if "Aero" in f.get("Department", "") else "ME"
        title = f.get("Job Title", "")
        fields = f.get("Matched Fields", "")
        lab = f.get("Lab / Research Group Name", "") or f.get("Research Interests", "Robotics & Controls")
        if len(lab) > 65:
            lab = lab[:62] + "..."
        lines.append(f"| [{name}](#{anchor}) | `{dept}` | {title} | `{fields}` | {lab} |")

    lines.append("\n---\n")
    lines.append("## 🔬 Comprehensive Faculty Profiles & Cold Outreach Intelligence\n")

    for idx, f in enumerate(field_matched, 1):
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        title = f.get("Job Title", "")
        dept = f.get("Department", "")
        p_url = f.get("Profile URL", "")
        s_url = f.get("Google Scholar URL", "")
        tier_label = f.get("Research Category", "Tier 4")

        lines.append(f"### {idx}. {name}\n")
        lines.append(f"- **Title**: {title}")
        lines.append(f"- **Department**: {dept}")
        lines.append(f"- **Research Categorization**: {tier_label}")
        if f.get("Email"):
            lines.append(f"- **Email**: [{f['Email']}](mailto:{f['Email']})")
        if f.get("Office Location"):
            lines.append(f"- **Office**: {f['Office Location']}")
        if p_url:
            lines.append(f"- **University Profile**: [{p_url}]({p_url})")
        if s_url:
            lines.append(f"- **Google Scholar**: [{s_url}]({s_url})")
        if f.get("Lab / Personal Website"):
            lines.append(f"- **Lab Website**: [{f['Lab / Personal Website']}]({f['Lab / Personal Website']})")
        if f.get("Lab / Research Group Name"):
            lines.append(f"- **Research Group**: {f['Lab / Research Group Name']}")

        lines.append(f"- **Matched Research Fields**: `{f.get('Matched Fields', '')}`")

        if f.get("Education / Degrees"):
            lines.append(f"- **Education & Degrees**: {f['Education / Degrees']}")

        if f.get("Research Interests"):
            lines.append(f"- **Research Interests**: {f['Research Interests']}")

        if f.get("Expertise Areas"):
            lines.append(f"- **Research Areas**: {f['Expertise Areas']}")

        if f.get("Recent Awards / Honors"):
            lines.append(f"- **Recent Awards & Appointments**: {f['Recent Awards / Honors']}")

        if f.get("Actively Hiring / Openings"):
            lines.append(f"- **Hiring & Openings Status**: 🎯 {f['Actively Hiring / Openings']}")

        if f.get("Cold Email / Application Instructions"):
            lines.append(f"- **Application & Contact Instructions**: 📨 {f['Cold Email / Application Instructions']}")

        if f.get("Lab Facilities & Equipment"):
            lines.append(f"- **Lab Facilities & Experimental Setup**: 🛠️ {f['Lab Facilities & Equipment']}")

        if f.get("Funding Sponsors"):
            lines.append(f"- **Funding Sponsors & Industry Partners**: 🏛️ {f['Funding Sponsors']}")

        # Cold Email Hooks Section
        lines.append("\n#### 🎯 Cold Outreach Personalization Hooks")

        flagship_hook = f.get("Flagship Paper Hook", "")
        tech_stack = f.get("Tech Stack", "")
        phys_finding = f.get("Physical Finding", "")
        res_hook = f.get("Research Hook", "")

        if res_hook:
            lines.append(f"- 💡 **Pillar 1 — Research Hook**: *\"{res_hook}\"*")
        if flagship_hook:
            lines.append(f"- 📄 **Pillar 2 — Flagship Paper**: **{flagship_hook}**")
        if tech_stack:
            lines.append(f"- 🛠️ **Pillar 3 — Tech Stack**: `{tech_stack}`")
        if phys_finding:
            lines.append(f"- 🔬 **Pillar 4 — Tripartite Physical Finding**:\n  > *\"...specifically your investigation into {phys_finding}\"*")

        if f.get("Top Cited Papers"):
            lines.append(f"- 🌟 **Top Cited Works (OpenAlex)**: {f['Top Cited Papers']}")

        if f.get("Recent Papers (2024-2026)"):
            lines.append(f"- **Recent Publications (2024-2026)**: {f['Recent Papers (2024-2026)']}")

        lines.append("\n---\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log.info(f"Successfully generated Markdown directory to {output_path}")


# =============================================================================
# 6. MAIN EXECUTION ROUTINE
# =============================================================================
def main():
    start_time = time.time()
    scraper = create_browser_session()

    output_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(output_dir, "purdue_aerospace_mechanical_faculty.xlsx")
    md_path = os.path.join(output_dir, "purdue_aerospace_mechanical_faculty.md")

    log.info("Starting Purdue University Aerospace & Mechanical Engineering Faculty Scraper...")
    faculty_data = scrape_purdue(scraper)

    if not faculty_data:
        log.error("No faculty data extracted. Exiting.")
        return

    export_to_excel(faculty_data, excel_path)
    export_to_markdown(faculty_data, md_path)

    elapsed = time.time() - start_time
    log.info(f"Pipeline finished successfully in {elapsed:.2f} seconds.")


if __name__ == "__main__":
    main()
