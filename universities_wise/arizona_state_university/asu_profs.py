import os
import re
import time
import logging
import urllib.parse
from typing import List, Dict, Any, Optional

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
    "Courses Taught",
    "Recent Awards / Honors",
    "Cold Email / Application Instructions",

    # 4. Academic Background & Research Focus
    "Research Interests",
    "Expertise Areas",
    "Research / Bio Summary",
    "Education / Degrees",

    # 5. Lab Intelligence & Active Opportunities
    "Lab / Research Group Name",
    "Lab / Personal Website",
    "Actively Hiring / Openings",
    "Target Skills / Prerequisites",
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

        # 1. Hiring / Openings & Cold Email Instructions
        if any(w in page_text.lower() for w in ["looking for motivated", "openings", "join us", "open position", "phd positions available", "prospective students"]):
            sentences = re.split(r'[.\n]', page_text)
            for s in sentences:
                s_clean = " ".join(s.split())
                if any(k in s_clean.lower() for k in ["looking for", "openings", "positions available", "join our group", "join the lab"]) and len(s_clean) < 140 and len(s_clean) > 15:
                    details["Actively Hiring / Openings"] = s_clean
                    break
                if any(k in s_clean.lower() for k in ["email me", "send your cv", "subject line", "cover letter"]) and 20 < len(s_clean) < 160:
                    details["Cold Email / Application Instructions"] = s_clean

            if not details["Actively Hiring / Openings"]:
                details["Actively Hiring / Openings"] = "Actively recruiting / Openings mentioned on lab site"

        # 2. Required Skills & Prereqs
        prereqs = []
        for sk in ["Python", "C++", "PyTorch", "TensorFlow", "ROS", "ROS2", "OpenFOAM", "MATLAB", "JAX", "ANSYS", "SolidWorks", "Linear Algebra", "CFD"]:
            pattern = r'\b' + re.escape(sk) + r'\b'
            if re.search(pattern, page_text):
                prereqs.append(sk)
        if prereqs:
            details["Target Skills / Prerequisites"] = ", ".join(prereqs)

        # 3. Funding Agencies & Sponsors
        sponsors = set()
        for sp in ["NSF", "NASA", "DARPA", "ONR", "AFOSR", "DOE", "NIH", "ARPA-E", "Lockheed Martin", "Boeing", "Honeywell", "Sandia National Laboratories"]:
            pattern = r'\b' + re.escape(sp) + r'\b'
            if re.search(pattern, page_text):
                sponsors.add(sp)
        if sponsors:
            details["Funding Sponsors"] = ", ".join(sorted(list(sponsors)))

        # 4. Code / GitHub / Bitbucket Repository
        repos = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if "github.com" in href or "bitbucket.org" in href or "gitlab.com" in href:
                if not any(ign in href for ign in ["github.com/google", "github.com/facebook", "github.com/twitter"]):
                    repos.add(href.rstrip("/"))
        if repos:
            details["Software / Code Repo"] = ", ".join(sorted(list(repos))[:2])

        # 5. Latest Project / Headline
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
                    "Courses Taught": "",
                    "Recent Awards / Honors": clean_awards,
                    "Cold Email / Application Instructions": cold_email_instructions,
                    "Research Interests": clean_interests if clean_interests else expertise_str,
                    "Expertise Areas": expertise_str,
                    "Research / Bio Summary": bio_summary,
                    "Education / Degrees": clean_edu,
                    "Lab / Research Group Name": lab_name,
                    "Lab / Personal Website": lab_website,
                    "Actively Hiring / Openings": hiring_status,
                    "Target Skills / Prerequisites": prereqs,
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
    for prof in results:
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
            time.sleep(0.08)

        # Third pass: Deep-scrape faculty lab websites for rich intelligence
        lab_url = prof.get("Lab / Personal Website", "")
        if lab_url:
            lab_details = scrape_deep_lab_site(scraper, lab_url)
            for k, v in lab_details.items():
                if v and (not prof.get(k) or prof.get(k) == ""):
                    prof[k] = v

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

    print("\n" + "=" * 95)
    print("ASU FACULTY & LAB SCRAPING COMPLETED (COLD EMAIL HOOKS INCLUDED)")
    print("=" * 95)
    print(f"Total Active Faculty (sorted by max keywords matched): {len(faculty)}")
    print(f"Field-Matched Faculty: {matched_count}")
    print(f"Direct Google Scholar User IDs: {with_id_count}")
    print(f"Faculty with Education / Degrees scraped: {with_edu_count}")
    print(f"Faculty with Courses Taught scraped: {with_courses_count}")
    print(f"Faculty with Recent Papers / Publications scraped: {with_papers_count}")
    print(f"Faculty with Awards / Honors scraped: {with_awards_count}")
    print(f"Faculty with Cold Email / Application Instructions: {with_instruct_count}")
    print(f"Faculty with Lab / Research Group Name scraped: {with_lab_name_count}")
    print(f"Faculty with Actively Hiring / Openings identified: {with_hiring_count}")
    print(f"Faculty with Target Skills / Prerequisites extracted: {with_prereqs_count}")
    print(f"Faculty with Funding Sponsors extracted: {with_funding_count}")
    print(f"Faculty with Software / Code Repositories extracted: {with_repo_count}")
    print(f"Faculty with Office Location scraped: {with_office_count}")
    print(f"Faculty with Lab / Personal Website scraped: {with_web_count}")
    print(f"Total Columns Configured Dynamically: {len(COLUMNS_CONFIG)}")
    print(f"Excel Workbook Path: {excel_path}")
    print("=" * 95)


if __name__ == "__main__":
    main()
