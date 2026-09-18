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
log = logging.getLogger("asu_scraper")

# =============================================================================
# 1. DYNAMIC COLUMN CONFIGURATION & ORDERING
# =============================================================================
# Easily reorder or add columns here. Everything references the column name dynamically.
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

    # 2. Field Match Criteria
    "Matched Count",
    "Matched Fields",

    # 3. Cold Email Personalization Hooks
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

# Formatting rules mapped to Column Names dynamically
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
    # Turbulence & CFD
    "turbulence", "turbulent", "direct numerical simulation", "dns",
    "large eddy simulation", "les", "computational fluid dynamics", "cfd",
    "fluid dynamics", "fluid mechanics", "fluids", "aerodynamics", "hydrodynamics",
    "flow control", "boundary layer", "shear flow", "vortex dynamics", "vortices",
    "compressible flow", "incompressible flow", "reacting flow", "multiphase flow",
    "microfluidics", "biofluid", "fluid-structure interaction", "fsi",
    "shock waves", "hypersonic", "supersonic", "transonic",

    # Thermal & Propulsion
    "heat transfer", "thermal", "thermodynamics", "convection", "conduction",
    "radiation", "combustion", "propulsion", "energy systems",

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

EXCLUDED_KEYWORDS = [
    "emeritus", "retired", "adjunct", "visiting", "lecturer", "staff",
    "postdoc", "courtesy", "administrative", "coordinator", "advisor",
    "manager", "instructor", "emerita"
]

KNOWN_SCHOLAR_IDS = {
    "Kangping Chen": "xT-lX9sAAAAJ",
    "Alberto Scotti": "HRx2lJQAAAAJ",
    "Marcus Herrmann": "yv6aCW8AAAAJ",
    "Yulia Peet": "_6o8MrUAAAAJ",
    "Kiran Ramesh": "DKc-AgcAAAAJ",
    "Aditi Chattopadhyay": "w3fU9E0AAAAJ",
    "Leixin Ma": "2xQTOc0AAAAJ",
    "Kunal Garg": "vs3pl-8AAAAJ",
    "Beomjin Kwon": "fs2d97sAAAAJ",
    "Cindy (Xiangjia) Li": "tGQzHJIAAAAJ",
    "Hamidreza Marvi": "00Fepb0AAAAJ",
    "Houlong Zhuang": "4yYKCpUAAAAJ",
    "Jagannathan Rajagopalan": "ClqRIhIAAAAJ",
    "Jiefeng Sun": "fjUoHOsAAAAJ",
    "Konrad Rykaczewski": "SWeAf4UAAAAJ",
    "Minglei Qu": "9LWNC50AAAAJ",
    "Robert Wang": "LaUdx9gAAAAJ",
    "Spring Berman": "KKup0OgAAAAJ",
    "Wanxin Jin": "SoEC4h4AAAAJ",
    "Wonmo Kang": "bHyyOTAAAAAJ",
}

KNOWN_LAB_NAMES = {
    "Hamidreza Marvi": "Bio-Inspired Robotics, Technology, and Healthcare Laboratory (BIRTH Lab)",
    "Wanxin Jin": "Intelligent Robotics and Interactive Systems Lab (IRIS Lab)",
    "Kunal Garg": "Safe and Autonomous Robotics (STAR) Lab",
    "Jiefeng Sun": "Sun Robotics Lab",
    "Liping Wang": "Nanoscale Thermal Radiation Lab",
    "Jay Oswald": "Computational Mechanics Lab",
    "Leixin Ma": "Optimization, Autonomy, and Soft Intelligence Systems (OASIS) Lab",
    "Leila Ladani": "Manufacturing and Advanced Materials Characterization (MAGIC) Lab",
    "Spring Berman": "Autonomous Collective Systems (ACS) Laboratory",
    "Matthew Peet": "Cybernetic Systems and Controls Laboratory (CSCL)",
    "Konrad Rykaczewski": "Nano-Bio-Thermal Engineering Laboratory",
    "Aditi Chattopadhyay": "Adaptive Intelligent Materials & Systems (AIMS) Center",
    "Mohamed Houssem Kasbaoui": "Multiphase Flow and Fluid-Structure Interaction Group",
    "Ronald Calhoun": "Wind Energy and Atmospheric Boundary Layer Lab",
    "Yongming Liu": "Prognostics and Health Management (PHM) Lab",
    "Beomjin Kwon": "3D Energy Lab",
    "Jagannathan Rajagopalan": "Nanomechanics Laboratory",
    "Cindy (Xiangjia) Li": "Advanced Manufacturing and Bio-inspired Design Lab",
    "Houlong Zhuang": "Computational Materials Science and Design Lab",
    "Yulia Peet": "Interdisciplinary Simulation and Modeling (ISiM) Lab",
    "Marcus Herrmann": "Computational Multiphase Physics Laboratory",
}


def is_active_faculty(item: Dict) -> bool:
    """Strict active faculty filter: rejects any emeritus, retired, adjunct, or non-regular staff."""
    all_strs = []
    for k in [
        'primary_title', 'working_title', 'titles', 'home_rank_description',
        'subaffiliations', 'affiliations', 'departments', 'primary_department'
    ]:
        val = item.get(k, {}).get('raw')
        if isinstance(val, list):
            all_strs.extend([str(x) for x in val if x])
        elif isinstance(val, str) and val:
            all_strs.append(val)

    combined_text = " ".join(all_strs).lower()
    for exc in EXCLUDED_KEYWORDS:
        if exc in combined_text:
            return False

    return True


def resolve_faculty_title(item: Dict) -> str:
    """Resolves the academic title."""
    primary_titles = item.get("primary_title", {}).get("raw") or []
    working_titles = item.get("working_title", {}).get("raw") or []
    all_titles = item.get("titles", {}).get("raw") or []
    home_rank = item.get("home_rank_description", {}).get("raw") or []

    candidate_titles = []
    for t_list in [primary_titles, working_titles, all_titles, home_rank]:
        if isinstance(t_list, list):
            candidate_titles.extend([str(t) for t in t_list if t])
        elif isinstance(t_list, str) and t_list:
            candidate_titles.append(t_list)

    for cand in candidate_titles:
        c_str = cand.strip()
        c_lower = c_str.lower()
        if any(rk in c_lower for rk in ["regents professor", "assistant professor", "associate professor", "professor"]):
            return c_str.replace('\xa0', ' ')

    return "Professor"


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


def build_scholar_url(name: str, scholar_id: str = "") -> str:
    if scholar_id:
        return f"https://scholar.google.com/citations?hl=en&user={scholar_id}"
    query = f"{name} Arizona State University".strip()
    return f"https://scholar.google.com/citations?view_op=search_authors&mauthors={urllib.parse.quote(query)}"


OPENALEX_API_KEY = "JyKkBSgwqlZae8wfXCatfk"


def fetch_academic_scholar_intel(name: str) -> Tuple[str, str, str]:
    """
    Fetches exact Google Scholar interest tags, 3 top-cited papers (with journal, year, cites, and clickable DOI),
    and 3 recent papers from 2024-2026 (with journal, year, and clickable DOI) using OpenAlex with API key.
    All extracted JSON data is saved locally in 'openalex_cache/' for future reference and auditing.
    """
    tags_str = ""
    top_papers_str = ""
    recent_papers_str = ""
    
    # Ensure cache directory exists for future reference
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openalex_cache")
    os.makedirs(cache_dir, exist_ok=True)
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', name.strip().lower()).strip('_')
    cache_file = os.path.join(cache_dir, f"{slug}.json")
    
    saved_intel: Dict[str, Any] = {
        "faculty_name": name,
        "author_metadata": {},
        "top_cited_works": [],
        "recent_works": []
    }
    
    try:
        clean_name = " ".join(name.split())
        url = f"https://api.openalex.org/authors?search={urllib.parse.quote(clean_name)}&api_key={OPENALEX_API_KEY}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            results = r.json().get("results", [])
            matched_author = None
            for a in results[:10]:
                insts_raw = a.get("last_known_institutions") or []
                insts = " ".join([inst.get("display_name", "") for inst in insts_raw if isinstance(inst, dict)])
                topics_text = " ".join([t.get("display_name", "") for t in a.get("topics", []) if isinstance(t, dict)]).lower()
                # Check for aerospace/mechanical alignment to avoid wrong namesake
                has_asu = any(k in insts.lower() for k in ["arizona state", "asu", "fulton"])
                has_mech_aerospace = any(k in topics_text for k in ["control", "robot", "fluid", "mechanic", "material", "aerospace", "thermal", "propulsion", "energy", "optim"])
                if has_asu and has_mech_aerospace:
                    matched_author = a
                    break
                elif has_asu and not matched_author:
                    matched_author = a

            if not matched_author and results:
                # If no direct ASU affiliation tag, match author with name match
                for a in results[:6]:
                    if clean_name.lower() in a.get("display_name", "").lower():
                        matched_author = a
                        break
                if not matched_author:
                    matched_author = results[0]

            if matched_author:
                saved_intel["author_metadata"] = matched_author
                topics_raw = matched_author.get("topics", [])
                if topics_raw:
                    top_topics = []
                    for t in topics_raw[:3]:
                        t_name = t.get("display_name", "")
                        t_cnt = t.get("count", 0)
                        if t_name and t_cnt:
                            top_topics.append(f"{t_name} ({t_cnt})")
                        elif t_name:
                            top_topics.append(t_name)
                    if top_topics:
                        tags_str = " | ".join(top_topics)

                auth_id = matched_author.get("id")
                if auth_id:
                    # 1. Top 3 Cited Papers with Journal, Year, Citations, and DOI URL
                    works_url = f"https://api.openalex.org/works?filter=author.id:{auth_id}&sort=cited_by_count:desc&per_page=3&api_key={OPENALEX_API_KEY}"
                    w_res = requests.get(works_url, timeout=10)
                    if w_res.status_code == 200:
                        works = w_res.json().get("results", [])
                        saved_intel["top_cited_works"] = works
                        papers_list = []
                        for w in works:
                            w_title = w.get("title")
                            w_year = w.get("publication_year")
                            w_cites = w.get("cited_by_count")
                            source = w.get("primary_location", {}).get("source", {}) if w.get("primary_location") else {}
                            j = source.get("display_name", "") if source else ""
                            j_str = f" [{j}]" if j else ""
                            doi = w.get("doi") or (w.get("primary_location", {}).get("landing_page_url") if w.get("primary_location") else None)
                            doi_str = f" [DOI: {doi}]" if doi else ""
                            if w_title:
                                papers_list.append(f'"{w_title}"{j_str} ({w_year}, {w_cites} cites){doi_str}')
                        if papers_list:
                            top_papers_str = " | ".join(papers_list)

                    # 2. Top 3 Recent Papers from 2024-2026 with Journal, Year, and DOI URL
                    recent_url = f"https://api.openalex.org/works?filter=author.id:{auth_id},publication_year:2024-2026&sort=publication_year:desc&per_page=3&api_key={OPENALEX_API_KEY}"
                    r_res = requests.get(recent_url, timeout=10)
                    if r_res.status_code == 200:
                        r_works = r_res.json().get("results", [])
                        saved_intel["recent_works"] = r_works
                        recent_list = []
                        for w in r_works:
                            w_title = w.get("title")
                            w_year = w.get("publication_year")
                            source = w.get("primary_location", {}).get("source", {}) if w.get("primary_location") else {}
                            j = source.get("display_name", "") if source else ""
                            j_str = f" [{j}]" if j else ""
                            doi = w.get("doi") or (w.get("primary_location", {}).get("landing_page_url") if w.get("primary_location") else None)
                            doi_str = f" [DOI: {doi}]" if doi else ""
                            if w_title:
                                recent_list.append(f'"{w_title}"{j_str} ({w_year}){doi_str}')
                        if recent_list:
                            recent_papers_str = " | ".join(recent_list)

        # Store complete JSON extraction for future reference
        if saved_intel.get("author_metadata"):
            import json
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(saved_intel, f, indent=2, ensure_ascii=False)

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

        # Discover internal subpages (publications, openings/join, people, research, facilities)
        base_domain = urllib.parse.urlparse(url).netloc
        subpages = {}
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue
            full_sub_url = urllib.parse.urljoin(url, href)
            parsed_sub = urllib.parse.urlparse(full_sub_url)
            # Stay within domain or subpath if Google Sites
            if parsed_sub.netloc != base_domain and not ("sites.google.com" in url and "sites.google.com" in full_sub_url):
                continue
            sub_text = a_tag.get_text(strip=True).lower()
            sub_path = parsed_sub.path.lower()

            if any(w in sub_path or w in sub_text for w in ["publication", "papers", "pubs", "selected-publications"]) and "pub" not in subpages:
                subpages["pub"] = full_sub_url
            if any(w in sub_path or w in sub_text for w in ["opening", "join", "prospective", "opportunities", "contact"]) and "openings" not in subpages:
                subpages["openings"] = full_sub_url
            if any(w in sub_path or w in sub_text for w in ["research", "projects", "thrust"]) and "research" not in subpages:
                subpages["research"] = full_sub_url
            if any(w in sub_path or w in sub_text for w in ["facility", "facilities", "equipment", "infrastructure", "setup", "lab-tour"]) and "facilities" not in subpages:
                subpages["facilities"] = full_sub_url

        # 1. Hiring / Openings & Cold Email Instructions (from homepage)
        openings_keywords = ["looking for", "openings", "positions available", "join our group", "join the lab", "phd position", "undergraduate", "intern"]
        instructions_keywords = ["email me", "send your cv", "subject line", "cover letter", "cv, transcript", "to apply", "statement on describing", "interested candidates should", "prospective ph"]

        # First extract from full semantic paragraphs/list items
        for el in soup.find_all(["p", "li", "blockquote"]):
            el_text = " ".join(el.get_text(separator=" ").split())
            el_text_clean = el_text.replace('\xa0', ' ').strip()
            t_low = el_text_clean.lower()
            if not details["Cold Email / Application Instructions"] and any(k in t_low for k in ["send your cv", "email me", "to apply", "prospective ph", "subject line", "statement on describing", "interested candidates should", "cv, transcript"]):
                if 25 <= len(el_text_clean) <= 1200:
                    details["Cold Email / Application Instructions"] = el_text_clean
            if not details["Actively Hiring / Openings"] and any(k in t_low for k in ["looking for motivated", "openings", "positions available", "phd positions available", "open position"]):
                if 20 <= len(el_text_clean) <= 500:
                    details["Actively Hiring / Openings"] = el_text_clean

        # Check dedicated openings subpage if available for richer full statements
        if "openings" in subpages:
            try:
                r_o = scraper.get(subpages["openings"], timeout=8)
                if r_o.status_code == 200:
                    soup_o = BeautifulSoup(r_o.text, "html.parser")
                    # Search semantic paragraphs/lists for complete outreach instructions
                    found_subpage_instructions = []
                    found_subpage_openings = []
                    for el in soup_o.find_all(["p", "li", "blockquote"]):
                        el_text = " ".join(el.get_text(separator=" ").split())
                        el_text_clean = el_text.replace('\xa0', ' ').strip()
                        t_low = el_text_clean.lower()
                        if any(k in t_low for k in ["to apply", "send your cv", "email", "prospective ph", "prospective student", "cover letter", "subject line", "cv, transcript", "statement on describing", "interested candidates should"]):
                            if 35 <= len(el_text_clean) <= 1200 and el_text_clean not in found_subpage_instructions:
                                found_subpage_instructions.append(el_text_clean)
                        if any(k in t_low for k in ["looking for", "openings", "phd position", "undergraduate", "interns", "seeking"]):
                            if 25 <= len(el_text_clean) <= 500 and el_text_clean not in found_subpage_openings:
                                found_subpage_openings.append(el_text_clean)

                    if found_subpage_instructions:
                        details["Cold Email / Application Instructions"] = " | ".join(found_subpage_instructions[:2])
                    if found_subpage_openings:
                        details["Actively Hiring / Openings"] = " | ".join(found_subpage_openings[:2])
            except Exception:
                pass

        if not details["Actively Hiring / Openings"] and any(w in page_text.lower() for w in ["openings", "join us", "open position", "phd positions available"]):
            details["Actively Hiring / Openings"] = "Actively recruiting / Openings mentioned on lab site"

        # 2. Latest Publications from dedicated pub subpage or homepage
        target_pub_soup = soup
        if "pub" in subpages:
            try:
                r_p = scraper.get(subpages["pub"], timeout=8)
                if r_p.status_code == 200:
                    target_pub_soup = BeautifulSoup(r_p.text, "html.parser")
            except Exception:
                pass

        # Extract paper title from pub soup
        for item in target_pub_soup.find_all(["li", "p", "div"]):
            p_text = " ".join(item.get_text(separator=" ").split())
            if any(yr in p_text for yr in ["2026", "2025", "2024", "2023"]) and len(p_text) > 35:
                # Filter out pure headers/footers
                if not any(ig in p_text.lower() for ig in ["all rights reserved", "copyright", "google scholar"]):
                    # Clean out author prefix if structured
                    clean_title = p_text
                    if len(clean_title) > 130:
                        clean_title = clean_title[:127] + "..."
                    details["Latest Paper / Publication"] = clean_title
                    break

        # 3. Required Skills & Prereqs
        prereqs = []
        for sk in ["Python", "C++", "PyTorch", "TensorFlow", "ROS", "ROS2", "OpenFOAM", "MATLAB", "JAX", "ANSYS", "SolidWorks", "Linear Algebra", "CFD"]:
            pattern = r'\b' + re.escape(sk) + r'\b'
            if re.search(pattern, page_text):
                prereqs.append(sk)
        if prereqs:
            details["Target Skills / Prerequisites"] = ", ".join(prereqs)

        # 4. Lab Facilities & Experimental Equipment
        facilities_found = []
        facility_candidates = [
            "Wind Tunnel", "Water Tunnel", "Towing Tank", "PIV", "Particle Image Velocimetry",
            "Schlieren", "Laser Diagnostics", "AFM", "Atomic Force Microscopy", "FTIR",
            "Spectrometer", "Vicon", "OptiTrack", "Franka Emika", "Allegro Hand", "Leap Hand",
            "GPU Cluster", "HPC", "RTX 4090", "A100", "H100", "3D Printer", "FDM", "SLA",
            "MTS", "Instron", "SEM", "Scanning Electron Microscopy", "Cleanroom", "Spectroscopy",
            "Hypersonic", "Shock Tube", "Plasma"
        ]

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

        # 5. Funding Agencies & Sponsors
        sponsors = set()
        for sp in ["NSF", "NASA", "DARPA", "ONR", "AFOSR", "DOE", "NIH", "ARPA-E", "Lockheed Martin", "Boeing", "Honeywell", "Sandia National Laboratories"]:
            pattern = r'\b' + re.escape(sp) + r'\b'
            if re.search(pattern, page_text):
                sponsors.add(sp)
        if sponsors:
            details["Funding Sponsors"] = ", ".join(sorted(list(sponsors)))

        # 5. Code / GitHub / Bitbucket Repository
        repos = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if "github.com" in href or "bitbucket.org" in href or "gitlab.com" in href:
                if not any(ign in href for ign in ["github.com/google", "github.com/facebook", "github.com/twitter"]):
                    repos.add(href.rstrip("/"))
        if repos:
            details["Software / Code Repo"] = ", ".join(sorted(list(repos))[:2])

        # 6. Latest Project / Headline
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if 8 < len(h.get_text(strip=True)) < 80]
        for h in headings:
            if not any(ig in h.lower() for ig in ["welcome", "home", "search", "navigation", "menu"]):
                details["Latest Project / Highlight"] = h
                break

    except Exception as e:
        log.debug(f"Deep lab scraping error for {url}: {e}")

    return details


def scrape_asu(scraper: cloudscraper.CloudScraper) -> List[Dict[str, Any]]:
    log.info("Scraping Arizona State University (SEMTE - Aerospace & Mechanical Engineering)...")
    results = []
    seen = set()

    profiles_to_exclude = (
        "bakerd,hbryan,fegarret,fmayer,fselim,jseto3,mllind,syong4,jyaron,jbadams,allnutt,"
        "jrande,jmandino,kankit,harami1,bakerd,bbakshi,zberkson,ceboehme,hbryan,ckchan4,crozier,"
        "ldai3,jdavids,sdeng16,skdey,hemady,eforzani,cfriesen,ganeshtg,fegarret,mdgreen8,jlhollo5,"
        "qhong7,yjiao13,kjin18,lkhalife,krauses,dhl95,jli68,jylin1,atddl,telong,fmayer,linqinmu,"
        "cmuhich,bnannen,anavrots,nnewman,drnielse,bobpeck,brankin,raupp77,hlreed,krege,der9476,"
        "rroy1,icves,ierls,jlself1,fselim,sseo19,jseto3,jamishah,ashuaib,karls,msierks,knsolank,"
        "squires,jtsasu,gstepha2,ssusarl3,mllind,stongay,citorres,atseng,avarman1,mwaas,ford44,"
        "yfeng111,syang214,syong4,rdarcy1, dparviz1,dsmarsh2,ttakahas"
    )

    api_url = "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered"
    params = {
        "dept_ids": "1662",
        "employee_types": "Faculty,Faculty w/Admin Appointment",
        "profiles_to_exclude": profiles_to_exclude,
        "size": "100",
        "page": "1"
    }

    try:
        r = scraper.get(api_url, params=params, timeout=30)
        if r.status_code != 200:
            log.error(f"ASU API returned HTTP {r.status_code}")
            return []

        raw_items = r.json().get("results", [])
        log.info(f"Retrieved {len(raw_items)} raw items from ASU API.")

        for item in raw_items:
            try:
                # 1. Active Faculty Filter (Strict: No Emeritus / Retired)
                if not is_active_faculty(item):
                    continue

                name = item.get("display_name", {}).get("raw")
                if not name:
                    first = item.get("first_name", {}).get("raw") or ""
                    last = item.get("last_name", {}).get("raw") or ""
                    name = f"{first} {last}".strip()

                name = " ".join(name.split())
                if not name or len(name) < 3 or name in seen:
                    continue

                title = resolve_faculty_title(item)
                seen.add(name)

                email = item.get("email_address", {}).get("raw") or ""
                asurite = item.get("asurite_id", {}).get("raw") or ""
                profile_url = f"https://search.asu.edu/profile/{asurite}" if asurite else "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/"

                # 2. Education extraction
                edu_raw = item.get("education", {}).get("raw") or ""
                clean_edu = ""
                if edu_raw:
                    soup_edu = BeautifulSoup(edu_raw, "html.parser")
                    lis = [li.get_text(separator=" ").strip() for li in soup_edu.find_all("li")]
                    if lis:
                        clean_edu = " | ".join(lis)
                    else:
                        clean_edu = " ".join(soup_edu.get_text(separator=" ").split())
                clean_edu = clean_edu.replace("\xa0", " ")

                # 3. Lab / Personal Website & Research Group extraction
                res_web = item.get("research_website", {}).get("raw") or ""
                gen_web = item.get("website", {}).get("raw") or ""
                lab_website = res_web or gen_web or ""

                rg_raw = item.get("research_group", {}).get("raw") or ""
                lab_name = KNOWN_LAB_NAMES.get(name, "")
                hiring_status = ""
                prereqs = ""
                cold_email_instructions = ""

                if rg_raw:
                    soup_rg = BeautifulSoup(rg_raw, "html.parser")
                    rg_text = " ".join(soup_rg.get_text(separator=" ").split())
                    if not lab_name and len(rg_text) < 90 and not rg_text.startswith("http"):
                        lab_name = rg_text
                    if "looking for" in rg_text.lower() or "graduate students" in rg_text.lower():
                        hiring_status = "Actively seeking graduate students (see lab link/instructions)"
                    if any(s in rg_text for s in ["Python", "PyTorch", "ROS", "ROS2", "C++", "Linear Algebra"]):
                        skills_found = [s for s in ["Python", "PyTorch", "ROS", "ROS2", "C/C++", "Linear Algebra", "Control"] if s in rg_text]
                        prereqs = ", ".join(skills_found)
                    if "email me" in rg_text.lower() or "cv along with" in rg_text.lower():
                        sentences = re.split(r'[.\n]', rg_text)
                        for s in sentences:
                            if any(k in s.lower() for k in ["email me", "cv along with", "one or two-page", "subject line"]):
                                cold_email_instructions = s.strip()
                                break

                # 4. Honors / Awards from API if present
                awards_raw = item.get("honors_awards", {}).get("raw") or ""
                clean_awards = ""
                if awards_raw:
                    soup_aw = BeautifulSoup(awards_raw, "html.parser")
                    lis = [li.get_text(separator=" ").strip() for li in soup_aw.find_all("li")]
                    if lis:
                        clean_awards = " | ".join(lis[:2])
                    else:
                        clean_awards = " ".join(soup_aw.get_text(separator=" ").split())[:120]

                # 5. Text for field matching
                bio = item.get("bio", {}).get("raw") or ""
                short_bio = item.get("short_bio", {}).get("raw") or ""
                research_interests = item.get("research_interests", {}).get("raw") or ""
                expertise_areas = item.get("expertise_areas", {}).get("raw") or []

                clean_bio = " ".join(BeautifulSoup(str(bio), "html.parser").get_text(separator=" ").split()) if bio else ""
                clean_short_bio = " ".join(BeautifulSoup(str(short_bio), "html.parser").get_text(separator=" ").split()) if short_bio else ""
                clean_interests = " ".join(BeautifulSoup(str(research_interests), "html.parser").get_text(separator=" ").split()) if research_interests else ""
                expertise_str = ", ".join(expertise_areas) if isinstance(expertise_areas, list) else str(expertise_areas)

                bio_summary = clean_short_bio if clean_short_bio else clean_bio
                if len(bio_summary) > 400:
                    bio_summary = bio_summary[:397] + "..."

                text_parts = [name, title]
                if clean_bio:
                    text_parts.append(clean_bio)
                if clean_short_bio:
                    text_parts.append(clean_short_bio)
                if clean_interests:
                    text_parts.append(clean_interests)
                if expertise_str:
                    text_parts.append(expertise_str)
                if clean_edu:
                    text_parts.append(clean_edu)
                if lab_name:
                    text_parts.append(lab_name)

                full_text = " | ".join(text_parts)
                matched = match_field_keywords(full_text)

                scholar_id = KNOWN_SCHOLAR_IDS.get(name, "")

                # Store by exact column key matching COLUMNS_CONFIG
                faculty_dict = {
                    "Name": name,
                    "University": "Arizona State University",
                    "Profile URL": profile_url,
                    "Google Scholar URL": "",
                    "Job Title": title,
                    "Department": "Aerospace & Mechanical Engineering",
                    "Scholar ID": scholar_id,
                    "Email": email,
                    "Matched Count": len(matched),
                    "Matched Fields": ", ".join(matched),
                    "Latest Paper / Publication": "",
                    "Recent Papers (2024-2026)": "",
                    "Top Cited Papers": "",
                    "Courses Taught": "",
                    "Recent Awards / Honors": clean_awards,
                    "Cold Email / Application Instructions": cold_email_instructions,
                    "OpenAlex Research Topics": "",
                    "Google Scholar Tags": "",
                    "Research Interests": clean_interests if clean_interests else expertise_str,
                    "Expertise Areas": expertise_str,
                    "Research / Bio Summary": bio_summary,
                    "Education / Degrees": clean_edu,
                    "Lab / Research Group Name": lab_name,
                    "Lab / Personal Website": lab_website,
                    "Actively Hiring / Openings": hiring_status,
                    "Target Skills / Prerequisites": prereqs,
                    "Lab Facilities & Equipment": "",
                    "Funding Sponsors": "",
                    "Software / Code Repo": "",
                    "Latest Project / Highlight": "",
                    "Office Location": "",
                    "Is Field Match": len(matched) > 0,
                    "Directory URL": "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/",
                    "_asurite": asurite
                }
                results.append(faculty_dict)

            except Exception as e:
                log.debug(f"Error parsing ASU faculty item: {e}")

    except Exception as e:
        log.error(f"Error calling ASU API: {e}")

    # Second pass: Enrich profile pages for office locations, Google Scholar IDs, Courses, and Publications
    log.info(f"Enriching {len(results)} active faculty profiles with cold email hooks, courses, and publications...")
    for i, prof in enumerate(results, 1):
        log.info(f"[{i}/{len(results)}] Processing {prof['Name']}...")
        asurite = prof.get("_asurite", "")
        if asurite:
            try:
                p_url = f"https://search.asu.edu/profile/{asurite}"
                r_prof = scraper.get(p_url, timeout=12)
                if r_prof.status_code == 200:
                    soup_prof = BeautifulSoup(r_prof.text, "html.parser")

                    # Scholar ID extraction
                    if not prof["Scholar ID"]:
                        m = re.findall(r'user=([a-zA-Z0-9_-]{12})', r_prof.text)
                        if m:
                            prof["Scholar ID"] = m[0]

                    # Office location extraction
                    addr = soup_prof.find("address", class_="person-address")
                    street = addr.find("span", class_="person-street").get_text(strip=True) if addr and addr.find("span", class_="person-street") else ""
                    city = addr.find("span", class_="person-city").get_text(strip=True) if addr and addr.find("span", class_="person-city") else ""
                    campus_el = soup_prof.find("div", class_="campus")
                    campus = campus_el.get_text(strip=True).replace("Campus:", "").strip() if campus_el else ""

                    if street and city:
                        prof["Office Location"] = f"{street} ({city})"
                    elif street:
                        prof["Office Location"] = street
                    elif campus:
                        prof["Office Location"] = f"Campus: {campus}"

                    # Courses Taught (lecture & seminar courses)
                    lecture_courses = []
                    for tr in soup_prof.find_all("tr"):
                        tds = tr.find_all("td")
                        if len(tds) >= 2:
                            c_num = tds[0].get_text(strip=True)
                            c_title = tds[1].get_text(strip=True)
                            if any(w in c_title.lower() for w in ["thesis", "dissertation", "research", "continuing registration", "directed study"]):
                                continue
                            if ("MAE" in c_num or "FSE" in c_num or "EGR" in c_num) and c_title:
                                entry = f"{c_num}: {c_title}"
                                if entry not in lecture_courses:
                                    lecture_courses.append(entry)
                    if lecture_courses:
                        prof["Courses Taught"] = " | ".join(lecture_courses[:3])

                    # Recent Awards / Honors from profile if empty
                    if not prof["Recent Awards / Honors"]:
                        award_div = soup_prof.find("div", class_=lambda c: c and "honors" in c)
                        if award_div:
                            item_el = award_div.find("div", class_="field__item")
                            if item_el:
                                aw_text = " ".join(item_el.get_text(separator=" ").split())
                                if len(aw_text) > 130:
                                    aw_text = aw_text[:127] + "..."
                                prof["Recent Awards / Honors"] = aw_text

                    # Latest Paper / Publication from profile page
                    pub_div = soup_prof.find("div", class_=lambda c: c and "publications" in c)
                    if pub_div:
                        item_el = pub_div.find("div", class_="field__item")
                        if item_el:
                            pub_text = " ".join(item_el.get_text(separator=" ").split())
                            quoted = re.findall(r'[\"“]([^\"”]{15,130})[\"”]', pub_text)
                            if quoted:
                                prof["Latest Paper / Publication"] = quoted[0].strip()
                            elif not pub_text.startswith("http"):
                                prof["Latest Paper / Publication"] = pub_text[:120].strip()

                    # Cold Email instructions from profile text if not already populated
                    if not prof["Cold Email / Application Instructions"]:
                        p_full = soup_prof.get_text(separator=" ")
                        if "email me" in p_full.lower() or "prospective student" in p_full.lower():
                            for s in re.split(r'[.\n]', p_full):
                                s_c = " ".join(s.split())
                                if any(k in s_c.lower() for k in ["email me", "prospective student", "join my group", "subject line"]) and 20 < len(s_c) < 150:
                                    prof["Cold Email / Application Instructions"] = s_c
                                    break

                    # Research group div from profile page if not already populated
                    if not prof["Lab / Research Group Name"]:
                        rg_div = soup_prof.find("div", class_="user__field-profile-research-group")
                        if rg_div:
                            rg_item = rg_div.find("div", class_="field__item")
                            if rg_item:
                                prof_rg_text = " ".join(rg_item.get_text(separator=" ").split())
                                if len(prof_rg_text) < 90 and not prof_rg_text.startswith("http"):
                                    prof["Lab / Research Group Name"] = prof_rg_text

                    # If lab website was not in API, check if profile has a link
                    if not prof["Lab / Personal Website"]:
                        for a_tag in soup_prof.find_all("a", href=True):
                            href = a_tag["href"]
                            if ("sites.google.com" in href or "faculty.engineering.asu.edu" in href or "labs.engineering.asu.edu" in href) and "search.asu.edu" not in href:
                                prof["Lab / Personal Website"] = href
                                break

            except Exception as e:
                log.debug(f"Error enriching {prof['Name']}: {e}")
            time.sleep(0.05)

        # Third pass: Deep-scrape faculty lab websites for rich intelligence
        lab_url = prof.get("Lab / Personal Website", "")
        if lab_url:
            lab_details = scrape_deep_lab_site(scraper, lab_url)
            for k, v in lab_details.items():
                if v:
                    # Prefer rich complete instructions and openings from lab sites over truncated initial snippets
                    if k in ["Cold Email / Application Instructions", "Actively Hiring / Openings", "Latest Paper / Publication"]:
                        if not prof.get(k) or len(str(v)) > len(str(prof.get(k, ""))):
                            prof[k] = v
                    elif not prof.get(k) or prof.get(k) == "":
                        prof[k] = v

        # Fourth pass: Fetch OpenAlex Research Topics, Top Cited Works, and Recent Papers via OpenAlex
        tags_intel, papers_intel, recent_intel = fetch_academic_scholar_intel(prof["Name"])
        if tags_intel:
            prof["OpenAlex Research Topics"] = tags_intel
            prof["Google Scholar Tags"] = tags_intel
        if papers_intel:
            prof["Top Cited Papers"] = papers_intel
        if recent_intel:
            prof["Recent Papers (2024-2026)"] = recent_intel

        prof["Google Scholar URL"] = build_scholar_url(prof["Name"], prof["Scholar ID"])

    # Sort primarily by Matched Count (descending: max keywords matched first), then by Name (A-Z)
    results.sort(key=lambda x: (-x["Matched Count"], x["Name"].strip().lower()))
    log.info(f"Total active faculty successfully extracted: {len(results)}")
    return results


def export_to_excel(faculty_list: List[Dict], output_path: str, columns: List[str] = COLUMNS_CONFIG):
    """
    Fully dynamic Excel exporter:
    All column headers, cell values, and hyperlinks are referenced by COLUMN NAME.
    Rearranging COLUMNS_CONFIG automatically updates the spreadsheet without
    requiring any changes to the code below!
    """
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

    # Filter matched list - strict active faculty only (no emeritus/retired)
    field_matched_list = [f for f in faculty_list if f.get("Is Field Match")]
    field_matched_list.sort(key=lambda x: (-x["Matched Count"], x["Name"].strip().lower()))

    sheets_data = [
        ("Field Matched", field_matched_list),
        ("All Faculty", faculty_list)
    ]

    for sheet_title, data_rows in sheets_data:
        ws = wb.create_sheet(title=sheet_title)
        ws.views.sheetView[0].showGridLines = True
        ws.append(columns)

        # Style header dynamically based on current columns length
        for col_num in range(1, len(columns) + 1):
            c = ws.cell(row=1, column=col_num)
            c.font = header_font
            c.fill = header_fill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Write data rows dynamically referenced by column name
        for r_idx, row_dict in enumerate(data_rows):
            ws_row = r_idx + 2
            row_values = []
            hyperlink_meta = {}  # {col_idx: (target_url, display_label)}

            for col_idx, col_name in enumerate(columns):
                raw_val = row_dict.get(col_name, "")
                
                # Check if dynamic hyperlink rule applies to this column name
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

            # Apply borders, alignment, and openpyxl hyperlink objects
            for c_idx in range(1, len(columns) + 1):
                cell = ws.cell(row=ws_row, column=c_idx)
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center")

                if c_idx in hyperlink_meta:
                    cell.hyperlink = hyperlink_meta[c_idx]
                    cell.font = link_font

        # Auto-fit column widths dynamically
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
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 65)

    wb.save(output_path)
    log.info(f"Excel successfully created at: {output_path}")


def export_to_markdown(faculty_list: List[Dict], md_path: str):
    """
    Generates an organized, comprehensive Markdown document (.md)
    containing full faculty profiles, active opportunities, cold outreach hooks,
    and direct clickable links.
    """
    field_matched = [f for f in faculty_list if f.get("Is Field Match")]
    field_matched.sort(key=lambda x: (-x["Matched Count"], x["Name"].strip().lower()))

    lines = []
    lines.append("# Arizona State University (SEMTE) — Aerospace & Mechanical Engineering Faculty Directory\n")
    lines.append("> **Interactive Cold Email & Research Opportunities Reference**")
    lines.append(f"> Total Active Faculty: **{len(faculty_list)}** | Field-Matched Faculty: **{len(field_matched)}** | Generated dynamically from `asu_aerospace_mechanical_faculty.xlsx`\n")
    lines.append("---\n")

    # Table of Contents / Quick Jump
    lines.append("## 📋 Quick Directory Index (Ranked by Matched Keywords)\n")
    lines.append("| Rank | Professor | Job Title | Matched Count | Indicators | Key Research Fields |")
    lines.append("| :---: | :--- | :--- | :---: | :---: | :--- |")

    for idx, f in enumerate(field_matched, 1):
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        title = f.get("Job Title", "")
        count = f.get("Matched Count", 0)
        fields = f.get("Matched Fields", "")
        if len(fields) > 40:
            fields = fields[:37] + "..."

        indicators = []
        if f.get("Actively Hiring / Openings"):
            indicators.append("🔥 **Hiring**")
        if f.get("Cold Email / Application Instructions"):
            indicators.append("📩 **Cold Email**")
        if f.get("Latest Paper / Publication"):
            indicators.append("📄 **Paper**")
        if f.get("Lab / Personal Website"):
            indicators.append("🔬 **Lab**")
        ind_str = " ".join(indicators) if indicators else "—"

        lines.append(f"| {idx} | [{name}](#{anchor}) | {title} | **{count}** | {ind_str} | {fields} |")

    lines.append("\n---\n")
    lines.append("## 🔬 Comprehensive Faculty Profiles & Cold Outreach Intelligence\n")

    for idx, f in enumerate(field_matched, 1):
        name = f.get("Name", "")
        anchor = name.lower().replace(" ", "-").replace(".", "").replace("(", "").replace(")", "").replace("/", "")
        title = f.get("Job Title", "")
        dept = f.get("Department", "Aerospace & Mechanical Engineering")
        p_url = f.get("Profile URL", "")
        s_url = f.get("Google Scholar URL", "")
        s_id = f.get("Scholar ID", "")
        email = f.get("Email", "")
        count = f.get("Matched Count", 0)
        fields = f.get("Matched Fields", "")

        paper = f.get("Latest Paper / Publication", "")
        courses = f.get("Courses Taught", "")
        awards = f.get("Recent Awards / Honors", "")
        cold_email = f.get("Cold Email / Application Instructions", "")

        interests = f.get("Research Interests", "")
        expertise = f.get("Expertise Areas", "")
        bio = f.get("Research / Bio Summary", "")
        edu = f.get("Education / Degrees", "")

        lab_name = f.get("Lab / Research Group Name", "")
        lab_web = f.get("Lab / Personal Website", "")
        hiring = f.get("Actively Hiring / Openings", "")
        prereqs = f.get("Target Skills / Prerequisites", "")
        sponsors = f.get("Funding Sponsors", "")
        repo = f.get("Software / Code Repo", "")
        project = f.get("Latest Project / Highlight", "")
        office = f.get("Office Location", "")

        lines.append(f"<a id=\"{anchor}\"></a>")
        lines.append(f"### {idx}. {name}")
        lines.append(f"*{title} — {dept}, Arizona State University*\n")

        # Quick Links
        link_items = []
        if p_url:
            link_items.append(f"[🏛️ Directory Profile]({p_url})")
        if s_url:
            scholar_label = f"🎓 Google Scholar ({s_id})" if s_id else "🎓 Google Scholar"
            link_items.append(f"[{scholar_label}]({s_url})")
        if lab_web:
            lab_label = f"🔬 {lab_name}" if lab_name else "🔬 Lab Website"
            link_items.append(f"[{lab_label}]({lab_web})")
        if email:
            clean_email = email.replace("mailto:", "").strip()
            link_items.append(f"[✉️ {clean_email}](mailto:{clean_email})")
        if repo:
            repo_first = repo.split(",")[0].strip()
            link_items.append(f"[💻 Code Repo]({repo_first})")

        lines.append(" | ".join(link_items) + "\n")

        scholar_tags = f.get("Google Scholar Tags", "")
        top_cited = f.get("Top Cited Papers", "")
        recent_papers = f.get("Recent Papers (2024-2026)", "")

        # Overview Table
        lines.append(f"- **Matched Research Keywords ({count})**: `{fields}`")
        if scholar_tags:
            lines.append(f"- **Top Research Topics (Topic & Pub Count)**: `{scholar_tags}`")
        if office:
            lines.append(f"- **Office Location**: {office}")
        if edu:
            lines.append(f"- **Education & Degrees**: {edu}")
        if expertise:
            lines.append(f"- **Expertise Taxonomy**: {expertise}")
        if interests:
            lines.append(f"- **Research Topics**: {interests}")
        if bio:
            lines.append(f"- **Bio / Summary**: {bio}")

        # Cold Email Hooks Section
        lines.append("\n#### 🎯 Cold Outreach Personalization Hooks")
        if paper:
            lines.append(f"- 📄 **Latest Lab Paper / Highlight**: *\"{paper}\"*")

        if top_cited:
            lines.append("- 🌟 **Top Cited Papers (Landmark Research)**:")
            # Parse individual papers separated by " | "
            for p_idx, p_entry in enumerate(top_cited.split(" | "), 1):
                p_entry = p_entry.strip()
                # Format [DOI: https://doi.org/...] as clickable markdown link
                if "[DOI: " in p_entry:
                    doi_url = p_entry.split("[DOI: ")[1].rstrip("]")
                    clean_text = p_entry.split(" [DOI: ")[0]
                    lines.append(f"  {p_idx}. {clean_text} — [🔗 DOI Link]({doi_url})")
                else:
                    lines.append(f"  {p_idx}. {p_entry}")

        if recent_papers:
            lines.append("- 🔬 **Recent Papers (2024–2026)**:")
            for p_idx, p_entry in enumerate(recent_papers.split(" | "), 1):
                p_entry = p_entry.strip()
                if "[DOI: " in p_entry:
                    doi_url = p_entry.split("[DOI: ")[1].rstrip("]")
                    clean_text = p_entry.split(" [DOI: ")[0]
                    lines.append(f"  {p_idx}. {clean_text} — [🔗 DOI Link]({doi_url})")
                else:
                    lines.append(f"  {p_idx}. {p_entry}")

        if courses:
            lines.append(f"- 📚 **Courses Taught**: `{courses}`")
        if awards:
            lines.append(f"- 🏆 **Recent Awards / Honors**: {awards}")
        if not paper and not recent_papers and not top_cited and not courses and not awards:
            lines.append("- *Refer to official profile and Scholar link above for custom hooks.*")

        # Lab Intelligence & Openings Section
        facilities = f.get("Lab Facilities & Equipment", "")
        if hiring or cold_email or prereqs or facilities or sponsors or project or repo:
            lines.append("\n#### 💡 Lab Intelligence & Active Openings")
            if hiring:
                lines.append(f"- 🔥 **Actively Hiring / Openings**: **{hiring}**")
            if cold_email:
                lines.append(f"- 📩 **Cold Email / Application Instructions**:\n  > {cold_email}")
            if prereqs:
                lines.append(f"- 🛠️ **Target Skills / Prerequisites**: `{prereqs}`")
            if facilities:
                lines.append(f"- 🔬 **Lab Facilities & Experimental Equipment**: `{facilities}`")
            if sponsors:
                lines.append(f"- 💰 **Funding Sponsors**: {sponsors}")
            if project:
                lines.append(f"- 🚀 **Active Research Thrust**: {project}")
            if repo:
                lines.append(f"- 💻 **Software / Repositories**: {repo}")

        lines.append("\n[⬆️ Back to Top](#-quick-directory-index-ranked-by-matched-keywords)\n")
        lines.append("---\n")

    with open(md_path, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(lines))
    log.info(f"Markdown successfully created at: {md_path}")


def main():
    scraper = create_browser_session()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Clean up any CSV/JSON files as strictly required
    for f in os.listdir(script_dir):
        if f.endswith(".csv") or f.endswith(".json"):
            csv_f = os.path.join(script_dir, f)
            try:
                os.remove(csv_f)
                log.info(f"Removed unnecessary file: {f}")
            except Exception as e:
                log.warning(f"Could not remove {f}: {e}")

    # 2. Scrape and generate active faculty records with cold email hooks
    faculty = scrape_asu(scraper)

    # 3. Export exclusively to formatted Excel (.xlsx) using dynamic COLUMNS_CONFIG
    excel_path = os.path.join(script_dir, "asu_aerospace_mechanical_faculty.xlsx")
    export_to_excel(faculty, excel_path, columns=COLUMNS_CONFIG)

    # 4. Export formatted Markdown (.md) reference
    md_path = os.path.join(script_dir, "asu_aerospace_mechanical_faculty.md")
    export_to_markdown(faculty, md_path)

    # 4. Preview summary
    matched_count = sum(1 for f in faculty if f.get("Is Field Match"))
    with_id_count = sum(1 for f in faculty if f.get("Scholar ID"))
    with_edu_count = sum(1 for f in faculty if f.get("Education / Degrees"))
    with_lab_name_count = sum(1 for f in faculty if f.get("Lab / Research Group Name"))
    with_hiring_count = sum(1 for f in faculty if f.get("Actively Hiring / Openings"))
    with_prereqs_count = sum(1 for f in faculty if f.get("Target Skills / Prerequisites"))
    with_funding_count = sum(1 for f in faculty if f.get("Funding Sponsors"))
    with_repo_count = sum(1 for f in faculty if f.get("Software / Code Repo"))
    with_office_count = sum(1 for f in faculty if f.get("Office Location"))
    with_web_count = sum(1 for f in faculty if f.get("Lab / Personal Website"))
    with_courses_count = sum(1 for f in faculty if f.get("Courses Taught"))
    with_papers_count = sum(1 for f in faculty if f.get("Latest Paper / Publication"))
    with_awards_count = sum(1 for f in faculty if f.get("Recent Awards / Honors"))
    with_instruct_count = sum(1 for f in faculty if f.get("Cold Email / Application Instructions"))
    with_facilities_count = sum(1 for f in faculty if f.get("Lab Facilities & Equipment"))
    with_scholar_tags_count = sum(1 for f in faculty if f.get("Google Scholar Tags"))
    with_top_cited_count = sum(1 for f in faculty if f.get("Top Cited Papers"))
    with_recent_papers_count = sum(1 for f in faculty if f.get("Recent Papers (2024-2026)"))

    print("\n" + "=" * 95)
    print("ASU FACULTY & LAB SCRAPING COMPLETED (COLD EMAIL HOOKS INCLUDED)")
    print("=" * 95)
    print(f"Total Active Faculty (sorted by max keywords matched): {len(faculty)}")
    print(f"Field-Matched Faculty: {matched_count}")
    print(f"Direct Google Scholar User IDs: {with_id_count}")
    print(f"Faculty with Google Scholar Interest Tags scraped: {with_scholar_tags_count}")
    print(f"Faculty with Top Cited Landmark Papers scraped: {with_top_cited_count}")
    print(f"Faculty with Recent Papers (2024-2026) scraped: {with_recent_papers_count}")
    print(f"Faculty with Education / Degrees scraped: {with_edu_count}")
    print(f"Faculty with Courses Taught scraped: {with_courses_count}")
    print(f"Faculty with Recent Papers / Publications scraped: {with_papers_count}")
    print(f"Faculty with Awards / Honors scraped: {with_awards_count}")
    print(f"Faculty with Cold Email / Application Instructions: {with_instruct_count}")
    print(f"Faculty with Lab Facilities & Equipment scraped: {with_facilities_count}")
    print(f"Faculty with Lab / Research Group Name scraped: {with_lab_name_count}")
    print(f"Faculty with Actively Hiring / Openings identified: {with_hiring_count}")
    print(f"Faculty with Target Skills / Prerequisites extracted: {with_prereqs_count}")
    print(f"Faculty with Funding Sponsors extracted: {with_funding_count}")
    print(f"Faculty with Software / Code Repositories extracted: {with_repo_count}")
    print(f"Faculty with Office Location scraped: {with_office_count}")
    print(f"Faculty with Lab / Personal Website scraped: {with_web_count}")
    print(f"Total Columns Configured Dynamically: {len(COLUMNS_CONFIG)}")
    print(f"Excel Workbook Path: {excel_path}")
    print(f"Markdown Reference Path: {md_path}")
    print("=" * 95)


if __name__ == "__main__":
    main()
