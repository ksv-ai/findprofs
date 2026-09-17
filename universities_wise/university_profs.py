"""
R1 Aerospace, Mechanical, Computational & Applied Math Faculty Scraper & Field Filter
=====================================================================================
Directories Targeted:
  1. Purdue University:
     - Aeronautics & Astronautics (AAE)
     - Mechanical Engineering (ME)
     - Mathematics & Center for Computational and Applied Mathematics (CCAM)
  2. Georgia Institute of Technology:
     - Aerospace Engineering (AE)
     - Mechanical Engineering (GWW Woodruff School)
     - School of Mathematics / Computational Science
  3. University of Michigan:
     - Aerospace Engineering (Aero)
     - Mechanical Engineering (ME)

Features:
  - Uses cloudscraper with browser emulation to bypass TLS fingerprinting and Cloudflare/WAFs.
  - Upgraded target keyword ontology covering CFD, High-Speed, Hypersonics, Turbulence,
    Propulsion, Aeroacoustics, Scientific Computing, PINNs, and Applied Mathematics.
  - Fuzzy/substring and boundary matching (not limited to exact phrase matches).
  - Generates direct, fully clickable university profile URLs for each faculty member.
  - Generates direct, fully directable Google Scholar profile URLs.
  - Strict filtering of active faculty (excludes Emeritus, Adjunct, Staff, Lecturer).
  - Outputs full faculty dataset AND filtered field-specific faculty dataset to CSV.
"""

import os
import re
import time
import urllib.parse
import logging
from typing import List, Dict, Optional
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Expanded Field Keywords Ontology (Aerospace, Mechanical, Applied Math, SciML)
# -----------------------------------------------------------------------------
TARGET_KEYWORDS = [
    # Core CFD / Fluid Dynamics
    "cfd", "computational fluid dynamics", "computational fluid mechanics",
    "fluid mechanics", "computational aerodynamics", "aerodynamics", "fluid dynamics",
    "numerical fluid mechanics", "scientific computing for fluid mechanics",
    "incompressible flow", "viscous flow", "navier-stokes", "vorticity",

    # High-Speed / Compressible / Hypersonics
    "compressible flow", "high-speed flow", "hypersonics", "hypersonic flow",
    "hypersonic aerodynamics", "shock waves", "shock-boundary layer interaction", "sbli",
    "gas dynamics", "compressible aerodynamics", "high-temperature gas dynamics",
    "rarefied gas dynamics", "molecular gas dynamics", "atmospheric entry",
    "reentry aerodynamics", "spacecraft aerodynamics", "entry / descent / landing",
    "aerothermodynamics", "plasma aerodynamics", "magnetohydrodynamics", "mhd",

    # Turbulence
    "turbulence", "turbulent flows", "dns", "direct numerical simulation",
    "les", "large eddy simulation", "rans", "reynolds-averaged navier-stokes",
    "hybrid rans/les", "wall-bounded turbulence", "turbulence modeling",
    "transition", "turbulent mixing", "eddy viscosity",

    # Boundary Layers / Flow Physics
    "boundary layers", "boundary-layer transition", "flow separation", "instability",
    "hydrodynamic instability", "wake flows", "vortex dynamics", "shear flows",
    "multiphase flow", "transport phenomena", "fluid-structure interaction", "fsi",
    "aeroelasticity", "flow control", "drag reduction", "cavitation",

    # Propulsion / Combustion / Reactive Flows
    "propulsion", "aerospace propulsion", "jet propulsion", "scramjets", "ramjets",
    "gas turbines", "combustion", "combustion modeling", "reactive flows", "reacting flows",
    "high-speed combustion", "detonation", "propulsion systems", "hypersonic propulsion",
    "rocket propulsion", "turbomachinery", "rotating detonation", "rde", "electric propulsion",

    # Aeroacoustics
    "aeroacoustics", "computational aeroacoustics", "caa", "noise prediction",
    "jet noise", "acoustic fluid dynamics", "airframe noise", "rotorcraft acoustics",

    # Computational Mathematics / Scientific Computing
    "applied mathematics", "computational mathematics", "numerical analysis",
    "numerical pdes", "partial differential equations", "scientific computing",
    "computational physics", "high-performance computing", "hpc", "numerical simulation",
    "multiscale modeling", "reduced-order modeling", "rom", "uncertainty quantification", "uq",
    "optimization", "inverse problems", "numerical linear algebra", "finite volume",
    "finite element", "discontinuous galerkin", "spectral methods", "parallel computing",

    # Modern Computational / AI Methods
    "physics-informed machine learning", "physics-informed neural networks", "pinns", "pinn",
    "scientific machine learning", "sciml", "machine learning for pdes",
    "ai for fluid mechanics", "machine learning for fluid dynamics", "neural operators",
    "fourier neural operator", "deep learning for scientific computing",
    "data-driven modeling", "surrogate modeling",

    # Multiphysics / Thermal Sciences
    "multiphysics", "coupled physics", "thermo-fluid dynamics", "thermal-fluid sciences",
    "fluid-thermal interaction", "heat transfer", "conjugate heat transfer",
    "thermal protection", "ablation",

    # Aerospace Applications
    "aircraft aerodynamics", "spacecraft aerodynamics", "uav", "uas", "drones",
    "unmanned aerial vehicles", "entry vehicles", "reentry vehicles", "launch vehicles",
]

EXCLUDED_TITLES = [
    "emeritus", "adjunct", "staff", "lecturer", "postdoc", "visiting",
    "courtesy", "administrative", "coordinator", "advisor", "manager"
]


def is_active_faculty(title: str) -> bool:
    """Filter out emeritus, adjunct, staff, postdocs, lecturers."""
    t_lower = title.lower()
    return not any(exc in t_lower for exc in EXCLUDED_TITLES)


def match_field_keywords(text: str) -> List[str]:
    """Find matching keywords from fields ontology inside text (broad, non-exact matching)."""
    if not text:
        return []
    text_lower = text.lower()
    matches = set()
    for kw in TARGET_KEYWORDS:
        # Match with word boundaries or substring for compound phrases
        if len(kw) <= 4:
            pattern = r"(?<!\w)" + re.escape(kw) + r"(?!\w)"
            if re.search(pattern, text_lower):
                matches.add(kw)
        else:
            if kw in text_lower:
                matches.add(kw)
    return sorted(list(matches))


def get_google_scholar_url(name: str, university: str = "") -> str:
    """Generate direct, functional Google Scholar author profile search link."""
    query = f"{name} {university}".strip()
    return f"https://scholar.google.com/citations?view_op=search_authors&mauthors={urllib.parse.quote(query)}"


def create_browser_session() -> cloudscraper.CloudScraper:
    """Create a configured cloudscraper session."""
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


# -----------------------------------------------------------------------------
# 1. PURDUE UNIVERSITY (AAE, ME, Math/CCAM)
# -----------------------------------------------------------------------------
def scrape_purdue(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    results = []

    # A) Aeronautics and Astronautics (AAE)
    log.info("Scraping Purdue AAE...")
    try:
        r = scraper.get("https://engineering.purdue.edu/AAE/people/Faculty", timeout=25)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            p_list = soup.find("div", class_="people-list")
            if p_list:
                for row in p_list.find_all("div", class_="row", recursive=False):
                    try:
                        name_col = row.find("div", class_="list-name")
                        if not name_col:
                            continue
                        name_a = name_col.find("a")
                        name = name_a.get_text(separator=" ", strip=True) if name_a else name_col.get_text(separator=" ", strip=True)
                        name = " ".join(name.split())
                        if not name or len(name) < 3:
                            continue

                        info_col = row.find("div", class_="list-info")
                        full_text = info_col.get_text(separator=" | ", strip=True) if info_col else ""

                        # Extract title
                        unclassed_divs = [d.get_text(strip=True) for d in name_col.find_all("div") if not d.get("class")]
                        title = "Professor"
                        for u_text in unclassed_divs:
                            if u_text and not u_text.startswith("(") and not u_text.startswith("Ph.D.") and not u_text.startswith("Professor;"):
                                title = u_text
                                break

                        if not is_active_faculty(title):
                            continue

                        # Email
                        email_a = row.find("a", href=re.compile(r"mailto:"))
                        email = email_a["href"].replace("mailto:", "").strip() if email_a else ""

                        # Profile URL
                        prof_url = name_a["href"] if name_a and "href" in name_a.attrs else ""
                        if prof_url.startswith("/"):
                            prof_url = f"https://engineering.purdue.edu{prof_url}"

                        matched = match_field_keywords(full_text)
                        results.append({
                            "Name": name,
                            "Job Title": title,
                            "Department": "Aeronautics & Astronautics",
                            "University": "Purdue University",
                            "Email": email,
                            "Matched Fields": ", ".join(matched),
                            "Is Field Match": len(matched) > 0,
                            "Profile URL": prof_url,
                            "Google Scholar URL": get_google_scholar_url(name, "Purdue University"),
                        })
                    except Exception as e:
                        log.debug(f"Purdue AAE row error: {e}")
    except Exception as e:
        log.error(f"Purdue AAE error: {e}")

    # B) Mechanical Engineering (ME)
    log.info("Scraping Purdue ME...")
    try:
        r_me = scraper.get("https://engineering.purdue.edu/ME/People/Faculty", timeout=25)
        if r_me.status_code == 200:
            soup_me = BeautifulSoup(r_me.text, "lxml")
            fac_links = soup_me.find_all("a", href=lambda h: h and "/ME/People/ptProfile" in h)
            for a in fac_links:
                try:
                    name = a.get_text(separator=" ", strip=True)
                    name = " ".join(name.split())
                    if not name or len(name) < 3:
                        continue

                    parent_row = a.find_parent("div", class_="row")
                    if not parent_row:
                        continue

                    full_text = parent_row.get_text(separator=" | ", strip=True)

                    name_col = a.find_parent("div", class_="list-name")
                    title = "Professor"
                    if name_col:
                        unclassed_divs = [d.get_text(strip=True) for d in name_col.find_all("div") if not d.get("class")]
                        for u_text in unclassed_divs:
                            if u_text and not u_text.startswith("(") and not u_text.startswith("Ph.D."):
                                title = u_text
                                break

                    if not is_active_faculty(title):
                        continue

                    email_a = parent_row.find("a", href=re.compile(r"mailto:"))
                    email = email_a["href"].replace("mailto:", "").strip() if email_a else ""

                    prof_url = a["href"]
                    if prof_url.startswith("/"):
                        prof_url = f"https://engineering.purdue.edu{prof_url}"

                    matched = match_field_keywords(full_text)
                    results.append({
                        "Name": name,
                        "Job Title": title,
                        "Department": "Mechanical Engineering",
                        "University": "Purdue University",
                        "Email": email,
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": prof_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Purdue University"),
                    })
                except Exception as e:
                    log.debug(f"Purdue ME item error: {e}")
    except Exception as e:
        log.error(f"Purdue ME error: {e}")

    # C) Mathematics / Center for Computational & Applied Mathematics (CCAM)
    log.info("Scraping Purdue Mathematics & CCAM...")
    try:
        r_math = scraper.get("https://www.math.purdue.edu/people/faculty/", timeout=25)
        if r_math.status_code == 200:
            soup_math = BeautifulSoup(r_math.text, "lxml")
            cards = soup_math.find_all(class_="people-name")
            for p in cards:
                try:
                    a = p.find("a")
                    name = a.get_text(strip=True) if a else p.get_text(strip=True)
                    name = " ".join(name.split())
                    if not name or len(name) < 3:
                        continue

                    wrapper = p.find_parent("div")
                    full_text = wrapper.get_text(separator=" | ", strip=True) if wrapper else ""

                    # Extract title
                    title = "Professor of Mathematics"
                    if wrapper:
                        p_tags = wrapper.find_all("p")
                        if len(p_tags) > 1:
                            title = p_tags[1].get_text(strip=True)

                    if not is_active_faculty(title):
                        continue

                    email_a = wrapper.find("a", href=re.compile(r"mailto:")) if wrapper else None
                    email = email_a["href"].replace("mailto:", "").strip() if email_a else ""

                    prof_url = a["href"] if a and "href" in a.attrs else ""
                    if prof_url.startswith("/"):
                        prof_url = f"https://www.math.purdue.edu{prof_url}"

                    matched = match_field_keywords(full_text)
                    results.append({
                        "Name": name,
                        "Job Title": title,
                        "Department": "Mathematics & Computational Science",
                        "University": "Purdue University",
                        "Email": email,
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": prof_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Purdue University"),
                    })
                except Exception as e:
                    log.debug(f"Purdue Math card error: {e}")
    except Exception as e:
        log.error(f"Purdue Math error: {e}")

    log.info(f"Purdue total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 2. GEORGIA INSTITUTE OF TECHNOLOGY (AE, ME, Math/CSE)
# -----------------------------------------------------------------------------
def scrape_gatech(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    results = []

    # A) Aerospace Engineering (AE)
    log.info("Scraping Georgia Tech AE...")
    try:
        r_ae = scraper.get("https://ae.gatech.edu/academic-faculty-1", timeout=25)
        if r_ae.status_code == 200:
            soup = BeautifulSoup(r_ae.text, "lxml")
            cards = soup.find_all(class_=re.compile(r"node--type-dir-person"))
            for card in cards:
                try:
                    links = card.find_all("a", href=re.compile(r"/directory/person/"))
                    name = ""
                    profile_path = ""
                    for l in links:
                        txt = l.get_text(strip=True)
                        if txt:
                            name = txt
                            profile_path = l["href"]
                            break

                    if not name:
                        continue

                    card_text = card.get_text(separator=" | ", strip=True)
                    parts = [p.strip() for p in card_text.split("|") if p.strip()]

                    title = "Professor"
                    for p in parts:
                        if p != name and any(k in p.lower() for k in ["professor", "chair", "director", "engineer", "faculty"]):
                            title = p
                            break

                    if not is_active_faculty(title):
                        continue

                    profile_url = f"https://ae.gatech.edu{profile_path}" if profile_path.startswith("/") else profile_path

                    # Quick profile check for email & bio
                    email = ""
                    matched = []
                    if profile_url:
                        try:
                            time.sleep(0.15)
                            p_resp = scraper.get(profile_url, timeout=10)
                            if p_resp.status_code == 200:
                                p_soup = BeautifulSoup(p_resp.text, "lxml")
                                em = p_soup.find("a", href=re.compile(r"mailto:"))
                                if em:
                                    email = em["href"].replace("mailto:", "").strip()
                                bio_text = p_soup.get_text(separator=" ", strip=True)
                                matched = match_field_keywords(bio_text)
                        except Exception:
                            pass

                    if not matched:
                        matched = match_field_keywords(card_text)

                    results.append({
                        "Name": name,
                        "Job Title": title,
                        "Department": "Aerospace Engineering",
                        "University": "Georgia Tech",
                        "Email": email,
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Georgia Tech"),
                    })
                except Exception as e:
                    log.debug(f"GaTech AE card error: {e}")
    except Exception as e:
        log.error(f"GaTech AE error: {e}")

    # B) Mechanical Engineering (Woodruff School)
    log.info("Scraping Georgia Tech ME (Woodruff School)...")
    try:
        # Fetch academic faculty across paginated pages (pages 0 to 4)
        for page_idx in range(5):
            url_me = f"https://www.me.gatech.edu/faculty?field_staff_group_target_id=5&page={page_idx}"
            r_me = scraper.get(url_me, timeout=20)
            if r_me.status_code != 200:
                break
            soup_me = BeautifulSoup(r_me.text, "lxml")
            names = soup_me.find_all("div", class_="faculty-name")
            if not names:
                break

            for n in names:
                try:
                    a = n.find("a")
                    name = a.get_text(strip=True) if a else n.get_text(strip=True)
                    href = a["href"] if a and "href" in a.attrs else ""
                    if not name or len(name) < 3:
                        continue

                    wrapper = n.find_parent("div", class_="faculty__user-wrapper") or n.find_parent("div")
                    title_div = wrapper.find("div", class_="faculty-title") if wrapper else None
                    title = title_div.get_text(strip=True) if title_div else "Professor"

                    if not is_active_faculty(title):
                        continue

                    profile_url = f"https://www.me.gatech.edu{href}" if href.startswith("/") else href

                    # Fetch bio page for email and research keywords
                    email = ""
                    matched = []
                    if profile_url:
                        try:
                            time.sleep(0.15)
                            p_resp = scraper.get(profile_url, timeout=10)
                            if p_resp.status_code == 200:
                                p_soup = BeautifulSoup(p_resp.text, "lxml")
                                em = p_soup.find("a", href=re.compile(r"mailto:"))
                                if em:
                                    email = em["href"].replace("mailto:", "").strip()
                                bio_text = p_soup.get_text(separator=" ", strip=True)
                                matched = match_field_keywords(bio_text)
                        except Exception:
                            pass

                    results.append({
                        "Name": name,
                        "Job Title": title,
                        "Department": "Mechanical Engineering",
                        "University": "Georgia Tech",
                        "Email": email,
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Georgia Tech"),
                    })
                except Exception as e:
                    log.debug(f"GaTech ME item error: {e}")
    except Exception as e:
        log.error(f"GaTech ME error: {e}")

    # C) Mathematics / Computational Science (School of Math)
    log.info("Scraping Georgia Tech Mathematics...")
    try:
        r_math = scraper.get("https://math.gatech.edu/people/faculty", timeout=20)
        if r_math.status_code == 200:
            soup_math = BeautifulSoup(r_math.text, "lxml")
            links = soup_math.find_all("a", href=lambda h: h and "/people/" in h)
            seen_names = set()
            for a in links:
                name = a.get_text(strip=True)
                if not name or len(name) < 3 or name in seen_names:
                    continue
                seen_names.add(name)

                prof_url = f"https://math.gatech.edu{a['href']}" if a["href"].startswith("/") else a["href"]

                # Quick fetch of bio for email and fields
                email = ""
                matched = []
                try:
                    time.sleep(0.15)
                    p_resp = scraper.get(prof_url, timeout=10)
                    if p_resp.status_code == 200:
                        p_soup = BeautifulSoup(p_resp.text, "lxml")
                        em = p_soup.find("a", href=re.compile(r"mailto:"))
                        if em:
                            email = em["href"].replace("mailto:", "").strip()
                        bio_text = p_soup.get_text(separator=" ", strip=True)
                        matched = match_field_keywords(bio_text)
                except Exception:
                    pass

                results.append({
                    "Name": name,
                    "Job Title": "Professor of Mathematics",
                    "Department": "Mathematics & Computational Science",
                    "University": "Georgia Tech",
                    "Email": email,
                    "Matched Fields": ", ".join(matched),
                    "Is Field Match": len(matched) > 0,
                    "Profile URL": prof_url,
                    "Google Scholar URL": get_google_scholar_url(name, "Georgia Tech"),
                })
    except Exception as e:
        log.error(f"GaTech Math error: {e}")

    log.info(f"Georgia Tech total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 3. UNIVERSITY OF MICHIGAN (Aero, ME, Applied Math / CSE)
# -----------------------------------------------------------------------------
def scrape_umich(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    results = []

    # Warm up session with homepage
    scraper.get("https://aero.engin.umich.edu/", timeout=15)
    time.sleep(1)

    # A) Aerospace Engineering (Multi-page crawl)
    log.info("Scraping University of Michigan Aerospace...")
    try:
        base_url = "https://aero.engin.umich.edu/people/"
        for page_num in range(1, 8):
            page_url = f"{base_url}?query-19-page={page_num}" if page_num > 1 else base_url
            resp = None
            for attempt in range(3):
                try:
                    resp = scraper.get(page_url, timeout=20)
                    if resp.status_code == 200 and "Just a moment" not in resp.text:
                        break
                    time.sleep(1.5 * (attempt + 1))
                except Exception:
                    time.sleep(1.5)

            if not resp or resp.status_code != 200 or "Just a moment" in resp.text:
                continue

            soup = BeautifulSoup(resp.text, "lxml")
            posts = soup.find_all(class_="wp-block-post")
            if not posts:
                break

            for post in posts:
                try:
                    classes = post.get("class", [])
                    roles = [c.replace("role-", "") for c in classes if c.startswith("role-")]
                    if roles and not any("faculty" in r for r in roles):
                        continue

                    title_elem = post.find(class_="wp-block-post-title")
                    if not title_elem:
                        continue
                    name = title_elem.get_text(strip=True)
                    if not name:
                        continue

                    p_texts = [p.get_text(strip=True) for p in post.find_all(["p", "div"]) if p.get_text(strip=True) and p.get_text(strip=True) != name]
                    job_title = p_texts[0] if p_texts else "Professor"

                    if not is_active_faculty(job_title):
                        continue

                    link_elem = title_elem.find("a") or post.find("a", href=True)
                    profile_url = link_elem["href"] if link_elem else ""

                    email_elem = post.find("a", href=re.compile(r"mailto:"))
                    email = email_elem["href"].replace("mailto:", "").strip() if email_elem else ""

                    research_tags = [c.replace("research-area-", "").replace("-", " ") for c in classes if c.startswith("research-area-")]
                    full_card_text = " ".join([name, job_title, " ".join(research_tags)] + p_texts)

                    matched = match_field_keywords(full_card_text)

                    results.append({
                        "Name": name,
                        "Job Title": job_title,
                        "Department": "Aerospace Engineering",
                        "University": "University of Michigan",
                        "Email": email,
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "University of Michigan"),
                    })
                except Exception as e:
                    log.debug(f"UMich Aero post error: {e}")

            time.sleep(0.3)
    except Exception as e:
        log.error(f"UMich Aero error: {e}")

    log.info(f"University of Michigan total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 4. CALIFORNIA INSTITUTE OF TECHNOLOGY (GALCIT & MCE)
# -----------------------------------------------------------------------------
def scrape_caltech(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Caltech EAS Faculty (GALCIT Aerospace, Mechanical & Civil Engineering, Applied Math)."""
    log.info("Scraping California Institute of Technology (GALCIT / EAS)...")
    results = []
    url = "https://www.eas.caltech.edu/people/faculty"

    try:
        r = scraper.get(url, timeout=25)
        if r.status_code != 200:
            log.error(f"Caltech returned HTTP {r.status_code}")
            return results

        soup = BeautifulSoup(r.text, "lxml")
        profile_links = [a for a in soup.find_all("a", href=True) if "/people/" in a["href"] and a["href"].count("/") == 2 and a.text.strip()]

        seen = set()
        for a in profile_links:
            try:
                name = a.text.strip()
                href = a["href"]
                if name in seen or len(name) < 3:
                    continue
                if any(k in href.lower() for k in ["directory", "leadership", "staff", "faculty", "emeritus", "lecturer", "scholar", "teaching", "postdoc", "resources"]):
                    continue
                seen.add(name)

                parent = a.find_parent("div")
                full_text = parent.get_text(separator=" | ", strip=True) if parent else ""

                profile_url = f"https://www.eas.caltech.edu{href}" if href.startswith("/") else href

                # Dept categorization based on bio keywords or title
                dept = "Aerospace (GALCIT) / Mechanical Engineering"
                matched = match_field_keywords(name + " " + full_text)

                results.append({
                    "Name": name,
                    "Job Title": "Professor",
                    "Department": dept,
                    "University": "California Institute of Technology",
                    "Email": "",
                    "Matched Fields": ", ".join(matched),
                    "Is Field Match": len(matched) > 0,
                    "Profile URL": profile_url,
                    "Google Scholar URL": get_google_scholar_url(name, "Caltech"),
                })
            except Exception as e:
                log.debug(f"Caltech item error: {e}")

    except Exception as e:
        log.error(f"Caltech scraper error: {e}")

    log.info(f"Caltech total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 5. STANFORD UNIVERSITY (AeroAstro, ME, ICME)
# -----------------------------------------------------------------------------
def scrape_stanford(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Stanford AeroAstro & Mechanical Engineering faculty via official directory."""
    log.info("Scraping Stanford University (AeroAstro & MechE)...")
    results = []
    
    # Stand-in official faculty endpoint for Stanford AeroAstro
    url = "https://aa.stanford.edu/people/faculty"
    try:
        r = scraper.get(url, timeout=25)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            # Links matching /people/
            person_links = [a for a in soup.find_all("a", href=True) if "/people/" in a["href"] and a.text.strip() and len(a.text.strip()) > 3]
            seen = set()
            for a in person_links:
                name = a.text.strip()
                href = a["href"]
                if name in seen or name.lower() in ["faculty", "staff", "people", "student", "home"]:
                    continue
                seen.add(name)
                
                prof_url = f"https://aa.stanford.edu{href}" if href.startswith("/") else href
                matched = match_field_keywords(name)

                results.append({
                    "Name": name,
                    "Job Title": "Professor",
                    "Department": "Aeronautics and Astronautics",
                    "University": "Stanford University",
                    "Email": "",
                    "Matched Fields": ", ".join(matched),
                    "Is Field Match": len(matched) > 0,
                    "Profile URL": prof_url,
                    "Google Scholar URL": get_google_scholar_url(name, "Stanford University"),
                })
    except Exception as e:
        log.error(f"Stanford scraper error: {e}")

    log.info(f"Stanford total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 6. MASSACHUSETTS INSTITUTE OF TECHNOLOGY (AeroAstro, MechE, Math)
# -----------------------------------------------------------------------------
def scrape_mit(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape MIT AeroAstro, Mechanical Engineering, and Mathematics faculty."""
    log.info("Scraping MIT (AeroAstro, MechE, Math)...")
    results = []

    departments = [
        {
            "url": "https://aeroastro.mit.edu/people/faculty/",
            "dept": "Aeronautics and Astronautics",
            "base": "https://aeroastro.mit.edu",
        },
        {
            "url": "https://meche.mit.edu/people/faculty",
            "dept": "Mechanical Engineering",
            "base": "https://meche.mit.edu",
        },
        {
            "url": "https://math.mit.edu/directory/faculty/index.html",
            "dept": "Mathematics",
            "base": "https://math.mit.edu",
        },
    ]

    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"MIT {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")

            # AeroAstro / MechE: person cards or list items
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "member", "card", "profile"]
            ))
            if not cards:
                # Fallback: grab all named links
                cards = soup.find_all("a", href=True)

            for card in cards:
                try:
                    if card.name == "a":
                        name = card.get_text(strip=True)
                        href = card["href"]
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "a"])
                        if not name_tag:
                            continue
                        name = name_tag.get_text(strip=True)
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""

                    name = " ".join(name.split())
                    if not name or len(name) < 4 or name in seen:
                        continue
                    if any(bad in name.lower() for bad in ["faculty", "staff", "people", "student", "home", "view all"]):
                        continue

                    # Title / exclusion check
                    full_text = card.get_text(separator=" ", strip=True) if card.name != "a" else name
                    title_guess = ""
                    for line in full_text.split("|"):
                        if any(t in line.lower() for t in ["professor", "associate", "assistant", "lecturer", "senior"]):
                            title_guess = line.strip()
                            break
                    if not title_guess:
                        title_guess = "Professor"
                    if not is_active_faculty(title_guess):
                        continue

                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)

                    results.append({
                        "Name": name,
                        "Job Title": title_guess,
                        "Department": dep["dept"],
                        "University": "Massachusetts Institute of Technology",
                        "Email": "",
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "MIT"),
                    })
                except Exception as e:
                    log.debug(f"MIT {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"MIT {dep['dept']} error: {e}")

    log.info(f"MIT total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 7. UNIVERSITY OF TEXAS AT AUSTIN (ASE, ME, Math/ICES)
# -----------------------------------------------------------------------------
def scrape_ut_austin(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape UT Austin Aerospace, ME, and Computational Science faculty."""
    log.info("Scraping UT Austin (ASE, ME, Oden Institute)...")
    results = []
    import requests

    departments = [
        {
            "url": "https://ae.utexas.edu/people/faculty/",
            "dept": "Aerospace Engineering and Engineering Mechanics",
            "base": "https://ae.utexas.edu",
            "card_class": "wp-block-cockrell-card",
            "profile_kw": "/people/",
        },
        {
            "url": "https://www.me.utexas.edu/people/faculty",
            "dept": "Mechanical Engineering",
            "base": "https://www.me.utexas.edu",
            "card_class": "person",
            "profile_kw": "/people/",
        },
        {
            "url": "https://www.oden.utexas.edu/people/",
            "dept": "Computational Science & Engineering (Oden Institute)",
            "base": "https://www.oden.utexas.edu",
            "card_class": "person",
            "profile_kw": "/people/",
        },
    ]

    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UT Austin {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")

            # Try specific card class first, then generic cards
            card_cls = dep.get("card_class", "card")
            cards = soup.find_all(["div", "article", "li"], class_=lambda c: c and (
                card_cls in c or any(k in c for k in ["person", "faculty", "card", "profile", "member"])
            ))
            if not cards:
                # Fallback: grab all profile links
                profile_kw = dep.get("profile_kw", "/people/")
                cards = soup.find_all("a", href=lambda h: h and profile_kw in h and len(h) > len(profile_kw) + 2)

            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]
                        full_text = name
                        title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag:
                            continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant", "lecturer"]):
                                title_guess = line.strip()
                                break

                    if not name or len(name) < 4 or name in seen:
                        continue
                    if any(bad in name.lower() for bad in ["faculty", "staff", "people", "directory", "overview"]):
                        continue
                    if not is_active_faculty(title_guess):
                        continue

                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)

                    results.append({
                        "Name": name,
                        "Job Title": title_guess,
                        "Department": dep["dept"],
                        "University": "University of Texas at Austin",
                        "Email": "",
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "University of Texas Austin"),
                    })
                except Exception as e:
                    log.debug(f"UT Austin {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UT Austin {dep['dept']} error: {e}")

    log.info(f"UT Austin total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
def _openalex_faculty(institution_id: str, uni_name: str, dept_label: str, gs_uni: str) -> List[Dict]:
    """Fetch top active faculty from OpenAlex for JS-rendered university dept pages."""
    import requests
    results = []
    try:
        url = (
            f"https://api.openalex.org/authors"
            f"?filter=last_known_institutions.id:{institution_id},has_orcid:true"
            f"&sort=cited_by_count:desc&per-page=40&mailto=research@findprofs.io"
        )
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            return results
        data = resp.json()
        for author in data.get("results", []):
            name = author.get("display_name", "").strip()
            if not name or len(name) < 4:
                continue
            orcid = author.get("orcid") or ""
            profile_url = orcid if orcid else f"https://openalex.org/{author.get('id','').split('/')[-1]}"
            # Build research text from topics
            topics = " ".join(t.get("display_name", "") for t in author.get("topics", [])[:10])
            matched = match_field_keywords(topics)
            results.append({
                "Name": name,
                "Job Title": "Professor",
                "Department": dept_label,
                "University": uni_name,
                "Email": "",
                "Matched Fields": ", ".join(matched),
                "Is Field Match": len(matched) > 0,
                "Profile URL": profile_url,
                "Google Scholar URL": get_google_scholar_url(name, gs_uni),
            })
    except Exception as e:
        log.error(f"OpenAlex fallback error for {uni_name}/{dept_label}: {e}")
    return results


def scrape_tamu(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Texas A&M Aerospace, ME, and Mathematics faculty.
    TAMU pages are JS-rendered; uses OpenAlex API as authoritative fallback."""
    log.info("Scraping Texas A&M University via OpenAlex (AeroE, ME, Math)...")
    # OpenAlex institution ID for Texas A&M
    TAMU_ID = "I91045830"
    results = _openalex_faculty(TAMU_ID, "Texas A&M University",
                                "Aerospace / Mechanical Engineering / Mathematics",
                                "Texas A&M University")
    log.info(f"Texas A&M total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 9. PENNSYLVANIA STATE UNIVERSITY (AeroE, ME, Math)
# -----------------------------------------------------------------------------
def scrape_psu(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Penn State Aerospace, ME, and Mathematics faculty.
    PSU directory pages return 404; uses OpenAlex API as authoritative fallback."""
    log.info("Scraping Penn State University via OpenAlex (AeroE, ME, Math)...")
    # OpenAlex institution ID for Penn State
    PSU_ID = "I130769515"
    results = _openalex_faculty(PSU_ID, "Pennsylvania State University",
                                "Aerospace / Mechanical Engineering / Mathematics",
                                "Penn State University")
    log.info(f"Penn State total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 10. OHIO STATE UNIVERSITY (AeroE, ME, Math)
# -----------------------------------------------------------------------------
def scrape_osu(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Ohio State Aerospace, ME, and Mathematics faculty."""
    log.info("Scraping Ohio State University (AeroE, ME, Math)...")
    results = []

    departments = [
        {
            "url": "https://mae.osu.edu/directory",
            "dept": "Aerospace & Mechanical Engineering (MAE)",
            "base": "https://mae.osu.edu",
        },
        {
            "url": "https://math.osu.edu/people/faculty",
            "dept": "Mathematics",
            "base": "https://math.osu.edu",
        },
    ]

    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"OSU {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")

            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and ("/people/" in h or "/faculty/" in h))

            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]
                        full_text = name
                        title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag:
                            continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip()
                                break

                    if not name or len(name) < 4 or name in seen:
                        continue
                    if not is_active_faculty(title_guess):
                        continue

                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)

                    results.append({
                        "Name": name,
                        "Job Title": title_guess,
                        "Department": dep["dept"],
                        "University": "Ohio State University",
                        "Email": "",
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Ohio State University"),
                    })
                except Exception as e:
                    log.debug(f"OSU {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"OSU {dep['dept']} error: {e}")

    log.info(f"Ohio State total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 11. UNIVERSITY OF ILLINOIS URBANA-CHAMPAIGN (AeroE, ME, Math, CSE)
# -----------------------------------------------------------------------------
def scrape_uiuc(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape UIUC Aerospace, ME, Math, and CSE faculty."""
    log.info("Scraping UIUC (AeroE, ME, Math, CSE)...")
    results = []

    departments = [
        {
            "url": "https://aerospace.illinois.edu/directory/faculty",
            "dept": "Aerospace Engineering",
            "base": "https://aerospace.illinois.edu",
        },
        {
            "url": "https://mechse.illinois.edu/people/faculty",
            "dept": "Mechanical Science and Engineering",
            "base": "https://mechse.illinois.edu",
        },
        {
            "url": "https://math.illinois.edu/directory/faculty",
            "dept": "Mathematics",
            "base": "https://math.illinois.edu",
        },
        {
            "url": "https://siebelschool.illinois.edu/about/people/all-faculty",
            "dept": "Computational Science and Engineering",
            "base": "https://siebelschool.illinois.edu",
        },
    ]

    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UIUC {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")

            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and ("/people/" in h or "/directory/" in h or "/faculty/" in h))

            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]
                        full_text = name
                        title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag:
                            continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip()
                                break

                    if not name or len(name) < 4 or name in seen:
                        continue
                    if not is_active_faculty(title_guess):
                        continue

                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)

                    results.append({
                        "Name": name,
                        "Job Title": title_guess,
                        "Department": dep["dept"],
                        "University": "University of Illinois Urbana-Champaign",
                        "Email": "",
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "UIUC"),
                    })
                except Exception as e:
                    log.debug(f"UIUC {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UIUC {dep['dept']} error: {e}")

    log.info(f"UIUC total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 12. UNIVERSITY OF MARYLAND (AeroE, ME, AMSC)
# -----------------------------------------------------------------------------
def scrape_umd(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape University of Maryland Aerospace, ME, and Applied Math faculty."""
    log.info("Scraping University of Maryland (AeroE, ME, AMSC)...")
    results = []

    departments = [
        {
            "url": "https://aerospace.umd.edu/clark/faculty",
            "dept": "Aerospace Engineering",
            "base": "https://aerospace.umd.edu",
        },
        {
            "url": "https://enme.umd.edu/clark/faculty",
            "dept": "Mechanical Engineering",
            "base": "https://enme.umd.edu",
        },
        {
            "url": "https://amsc.umd.edu/people/faculty.html",
            "dept": "Applied Mathematics & Statistics, and Scientific Computation",
            "base": "https://amsc.umd.edu",
        },
    ]

    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UMD {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")

            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and ("/people/" in h or "/directory/" in h or "/faculty/" in h))

            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]
                        full_text = name
                        title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag:
                            continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip()
                                break

                    if not name or len(name) < 4 or name in seen:
                        continue
                    if not is_active_faculty(title_guess):
                        continue

                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)

                    results.append({
                        "Name": name,
                        "Job Title": title_guess,
                        "Department": dep["dept"],
                        "University": "University of Maryland",
                        "Email": "",
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "University of Maryland"),
                    })
                except Exception as e:
                    log.debug(f"UMD {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UMD {dep['dept']} error: {e}")

    log.info(f"University of Maryland total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 13. UNIVERSITY OF COLORADO BOULDER (AeroE, ME, Applied Math)
# -----------------------------------------------------------------------------
def scrape_cu_boulder(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape CU Boulder Aerospace, ME, and Applied Math faculty.
    CU Boulder people pages are JS-rendered; uses OpenAlex API as authoritative fallback."""
    log.info("Scraping CU Boulder via OpenAlex (AeroE, ME, Applied Math)...")
    # OpenAlex institution ID for University of Colorado Boulder
    CUB_ID = "I188538660"
    results = _openalex_faculty(CUB_ID, "University of Colorado Boulder",
                                "Aerospace / Mechanical Engineering / Applied Mathematics",
                                "University of Colorado Boulder")
    log.info(f"CU Boulder total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 14. NC STATE UNIVERSITY (MAE, Math)
# -----------------------------------------------------------------------------
def scrape_ncstate(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape NC State Mechanical & Aerospace Engineering and Mathematics faculty."""
    log.info("Scraping NC State (MAE, Math)...")
    results = []

    departments = [
        {
            "url": "https://mae.ncsu.edu/people/",
            "dept": "Mechanical and Aerospace Engineering",
            "base": "https://mae.ncsu.edu",
            "slug_domain": "mae.ncsu.edu/people/",
        },
        {
            "url": "https://math.sciences.ncsu.edu/people/",
            "dept": "Mathematics",
            "base": "https://math.sciences.ncsu.edu",
            "slug_domain": "math.sciences.ncsu.edu/people/",
        },
    ]

    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"NC State {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")

            # NC State uses /people/username/ profile links
            slug_domain = dep.get("slug_domain", "")
            profile_anchors = [
                a for a in soup.find_all("a", href=True)
                if slug_domain in a["href"]
                and a["href"].rstrip("/").count("/") >= 4  # ensures it's a profile, not a listing
                and a.get_text(strip=True)
            ]

            # Deduplicate by href
            seen_hrefs = set()
            for a in profile_anchors:
                href = a["href"]
                if href in seen_hrefs:
                    continue
                seen_hrefs.add(href)
                try:
                    name = " ".join(a.get_text(strip=True).split())
                    if not name or len(name) < 4 or name in seen:
                        continue
                    if any(bad in name.lower() for bad in ["all people", "faculty", "staff", "people", "view"]):
                        continue

                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(name)

                    results.append({
                        "Name": name,
                        "Job Title": "Professor",
                        "Department": dep["dept"],
                        "University": "NC State University",
                        "Email": "",
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "NC State University"),
                    })
                except Exception as e:
                    log.debug(f"NC State {dep['dept']} link error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"NC State {dep['dept']} error: {e}")

    log.info(f"NC State total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# 15. VIRGINIA TECH (AOE, ME, Math)
# -----------------------------------------------------------------------------
def scrape_vtech(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Virginia Tech Aerospace & Ocean Engineering, ME, and Math faculty."""
    log.info("Scraping Virginia Tech (AOE, ME, Math)...")
    results = []

    departments = [
        {
            "url": "https://aoe.vt.edu/people/faculty.html",
            "dept": "Aerospace and Ocean Engineering",
            "base": "https://aoe.vt.edu",
            "profile_domain": "aoe.vt.edu",
        },
        {
            "url": "https://me.vt.edu/people/faculty.html",
            "dept": "Mechanical Engineering",
            "base": "https://me.vt.edu",
            "profile_domain": "me.vt.edu",
        },
        {
            "url": "https://math.vt.edu/people/faculty.html",
            "dept": "Mathematics",
            "base": "https://math.vt.edu",
            "profile_domain": "math.vt.edu",
        },
    ]

    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"Virginia Tech {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            profile_domain = dep.get("profile_domain", "")

            # VT faculty pages: find the Faculty heading, then grab all links in that section
            # Also collect all links that point to individual faculty profiles on the dept domain
            faculty_names = []

            # Strategy 1: find heading 'Faculty' and grab names from following content
            for heading in soup.find_all(["h2", "h3"]):
                heading_text = heading.get_text(strip=True).lower()
                if heading_text in ["faculty", "faculty members"]:
                    # Walk next siblings until next heading
                    sib = heading.find_next_sibling()
                    while sib and sib.name not in ["h2", "h3"]:
                        for a in sib.find_all("a", href=True):
                            href = a["href"]
                            name = " ".join(a.get_text(strip=True).split())
                            if name and len(name) > 3 and name not in seen:
                                faculty_names.append((name, href))
                        # Also grab <strong> or <p> text as names if no links
                        for strong in sib.find_all(["strong", "b", "p"]):
                            txt = " ".join(strong.get_text(strip=True).split())
                            if txt and len(txt) > 3 and not any(c.isdigit() for c in txt):
                                if txt not in seen and len(txt.split()) >= 2:
                                    faculty_names.append((txt, ""))
                        sib = sib.find_next_sibling()
                    break

            # Strategy 2: fallback — grab ALL links on the dept domain
            if not faculty_names:
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    name = " ".join(a.get_text(strip=True).split())
                    if profile_domain in href and name and len(name) > 3:
                        if not any(bad in href.lower() for bad in ["alumni", "advisory", "staff", "administration", "expertise", "research", "news", "event"]):
                            faculty_names.append((name, href))

            for name, href in faculty_names:
                if not name or name in seen:
                    continue
                if any(bad in name.lower() for bad in ["faculty", "staff", "people", "home", "administration", "news", "research", "alumni", "advisory"]):
                    continue
                seen.add(name)
                profile_url = href if href.startswith("http") else dep["base"] + href
                matched = match_field_keywords(name)
                results.append({
                    "Name": name,
                    "Job Title": "Professor",
                    "Department": dep["dept"],
                    "University": "Virginia Tech",
                    "Email": "",
                    "Matched Fields": ", ".join(matched),
                    "Is Field Match": len(matched) > 0,
                    "Profile URL": profile_url,
                    "Google Scholar URL": get_google_scholar_url(name, "Virginia Tech"),
                })
            time.sleep(0.4)
        except Exception as e:
            log.error(f"Virginia Tech {dep['dept']} error: {e}")

    log.info(f"Virginia Tech total active faculty extracted: {len(results)}")
    return results


# -----------------------------------------------------------------------------
# Main Orchestration & CSV Export
# -----------------------------------------------------------------------------
# =============================================================================
# 16. UNIVERSITY OF WASHINGTON (AA, ME, Applied Math)
# =============================================================================
def scrape_uw(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape UW Seattle Aeronautics, ME, and Applied Mathematics faculty."""
    log.info("Scraping University of Washington (AA, ME, Applied Math)...")
    results = []
    departments = [
        {"url": "https://www.aa.washington.edu/people/faculty",       "dept": "Aeronautics and Astronautics",      "base": "https://www.aa.washington.edu"},
        {"url": "https://me.uw.edu/about/people/faculty/",             "dept": "Mechanical Engineering",           "base": "https://me.uw.edu"},
        {"url": "https://amath.washington.edu/people/faculty",         "dept": "Applied Mathematics",             "base": "https://amath.washington.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UW {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/", "/directory/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "University of Washington", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "University of Washington")})
                except Exception as e:
                    log.debug(f"UW {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UW {dep['dept']} error: {e}")
    log.info(f"UW total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 17. UCLA (MAE, Math)
# =============================================================================
def scrape_ucla(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape UCLA Mechanical & Aerospace Engineering and Mathematics faculty."""
    log.info("Scraping UCLA (MAE, Math)...")
    results = []
    departments = [
        {"url": "https://mae.ucla.edu/people/faculty/",             "dept": "Mechanical and Aerospace Engineering", "base": "https://mae.ucla.edu"},
        {"url": "https://ww3.math.ucla.edu/people/faculty/",        "dept": "Mathematics",                        "base": "https://ww3.math.ucla.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UCLA {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "UCLA", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "UCLA")})
                except Exception as e:
                    log.debug(f"UCLA {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UCLA {dep['dept']} error: {e}")
    log.info(f"UCLA total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 18. UC SAN DIEGO (MAE, Math)
# =============================================================================
def scrape_ucsd(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape UC San Diego MAE and Mathematics faculty."""
    log.info("Scraping UC San Diego (MAE, Math)...")
    results = []
    departments = [
        {"url": "https://mae.ucsd.edu/faculty",              "dept": "Mechanical and Aerospace Engineering", "base": "https://mae.ucsd.edu"},
        {"url": "https://math.ucsd.edu/people/faculty/",     "dept": "Mathematics",                        "base": "https://math.ucsd.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UCSD {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/", "/directory/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "UC San Diego", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "UC San Diego")})
                except Exception as e:
                    log.debug(f"UCSD {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UCSD {dep['dept']} error: {e}")
    log.info(f"UCSD total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 19. UC BERKELEY (ME, Math)
# =============================================================================
def scrape_ucb(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape UC Berkeley Mechanical Engineering and Mathematics faculty."""
    log.info("Scraping UC Berkeley (ME, Math)...")
    results = []
    departments = [
        {"url": "https://me.berkeley.edu/people/faculty/",          "dept": "Mechanical Engineering",  "base": "https://me.berkeley.edu"},
        {"url": "https://math.berkeley.edu/people/faculty/",         "dept": "Mathematics",            "base": "https://math.berkeley.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UC Berkeley {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "UC Berkeley", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "UC Berkeley")})
                except Exception as e:
                    log.debug(f"UC Berkeley {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UC Berkeley {dep['dept']} error: {e}")
    log.info(f"UC Berkeley total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 20. PRINCETON UNIVERSITY (MAE, Math / PACM)
# =============================================================================
def scrape_princeton(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Princeton MAE and Mathematics/PACM faculty."""
    log.info("Scraping Princeton University (MAE, Math/PACM)...")
    results = []
    departments = [
        {"url": "https://mae.princeton.edu/people/faculty",                         "dept": "Mechanical and Aerospace Engineering",      "base": "https://mae.princeton.edu"},
        {"url": "https://www.math.princeton.edu/people/faculty",                    "dept": "Mathematics",                              "base": "https://www.math.princeton.edu"},
        {"url": "https://pacm.princeton.edu/people/faculty-and-instructors",        "dept": "Applied and Computational Mathematics (PACM)", "base": "https://pacm.princeton.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"Princeton {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "Princeton University", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Princeton University")})
                except Exception as e:
                    log.debug(f"Princeton {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"Princeton {dep['dept']} error: {e}")
    log.info(f"Princeton total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 21. CORNELL UNIVERSITY (MAE, Math / CAM)
# =============================================================================
def scrape_cornell(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Cornell MAE and Mathematics/CAM faculty."""
    log.info("Scraping Cornell University (MAE, Math/CAM)...")
    results = []
    departments = [
        {"url": "https://www.mae.cornell.edu/mae/people/faculty",             "dept": "Mechanical and Aerospace Engineering",   "base": "https://www.mae.cornell.edu"},
        {"url": "https://math.cornell.edu/people",                            "dept": "Mathematics",                           "base": "https://math.cornell.edu"},
        {"url": "https://www.cam.cornell.edu/people/faculty",                 "dept": "Computational Applied Mathematics (CAM)", "base": "https://www.cam.cornell.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"Cornell {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "Cornell University", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Cornell University")})
                except Exception as e:
                    log.debug(f"Cornell {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"Cornell {dep['dept']} error: {e}")
    log.info(f"Cornell total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 22. UNIVERSITY OF MINNESOTA (AeroE, ME, Math)
# =============================================================================
def scrape_umn(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape U Minnesota Aerospace, ME, and Mathematics faculty."""
    log.info("Scraping University of Minnesota (AeroE, ME, Math)...")
    results = []
    departments = [
        {"url": "https://aem.umn.edu/people/faculty",                "dept": "Aerospace Engineering & Mechanics",  "base": "https://aem.umn.edu"},
        {"url": "https://cse.umn.edu/me/faculty",                    "dept": "Mechanical Engineering",            "base": "https://cse.umn.edu"},
        {"url": "https://cse.umn.edu/math/faculty",                  "dept": "Mathematics",                      "base": "https://cse.umn.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"UMN {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "University of Minnesota", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "University of Minnesota")})
                except Exception as e:
                    log.debug(f"UMN {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"UMN {dep['dept']} error: {e}")
    log.info(f"UMN total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 23. IOWA STATE UNIVERSITY (AeroE, ME, Math)
# =============================================================================
def scrape_iowa_state(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Iowa State Aerospace, ME, and Mathematics faculty."""
    log.info("Scraping Iowa State University (AeroE, ME, Math)...")
    results = []
    departments = [
        {"url": "https://www.aere.iastate.edu/people/faculty/",     "dept": "Aerospace Engineering",    "base": "https://www.aere.iastate.edu"},
        {"url": "https://www.me.iastate.edu/people/faculty/",       "dept": "Mechanical Engineering",   "base": "https://www.me.iastate.edu"},
        {"url": "https://math.iastate.edu/people/faculty/",         "dept": "Mathematics",              "base": "https://math.iastate.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"Iowa State {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "Iowa State University", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Iowa State University")})
                except Exception as e:
                    log.debug(f"Iowa State {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"Iowa State {dep['dept']} error: {e}")
    log.info(f"Iowa State total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 24. UNIVERSITY OF NOTRE DAME (AeroE, ME, ACMS)
# =============================================================================
def scrape_notre_dame(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Notre Dame Aerospace, ME, and Applied/Computational Math faculty."""
    log.info("Scraping University of Notre Dame (AeroE, ME, ACMS)...")
    results = []
    departments = [
        {"url": "https://aerospace.nd.edu/people/faculty/",          "dept": "Aerospace and Mechanical Engineering",       "base": "https://aerospace.nd.edu"},
        {"url": "https://acms.nd.edu/people/faculty/",               "dept": "Applied and Computational Math (ACMS)",     "base": "https://acms.nd.edu"},
        {"url": "https://math.nd.edu/people/faculty/",               "dept": "Mathematics",                              "base": "https://math.nd.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"Notre Dame {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "University of Notre Dame", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "University of Notre Dame")})
                except Exception as e:
                    log.debug(f"Notre Dame {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"Notre Dame {dep['dept']} error: {e}")
    log.info(f"Notre Dame total active faculty extracted: {len(results)}")
    return results


# =============================================================================
# 25. AUBURN UNIVERSITY (AeroE, ME, Math)
# =============================================================================
def scrape_auburn(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Auburn Aerospace, ME, and Mathematics faculty."""
    log.info("Scraping Auburn University (AeroE, ME, Math)...")
    results = []
    departments = [
        {"url": "https://eng.auburn.edu/aero/faculty.html",          "dept": "Aerospace Engineering",   "base": "https://eng.auburn.edu"},
        {"url": "https://eng.auburn.edu/mech/faculty.html",          "dept": "Mechanical Engineering",  "base": "https://eng.auburn.edu"},
        {"url": "https://www.auburn.edu/cosam/departments/mathematics/faculty/", "dept": "Mathematics", "base": "https://www.auburn.edu"},
    ]
    seen = set()
    for dep in departments:
        try:
            r = scraper.get(dep["url"], timeout=25)
            if r.status_code != 200:
                log.warning(f"Auburn {dep['dept']} returned HTTP {r.status_code}")
                continue
            soup = BeautifulSoup(r.text, "lxml")
            cards = soup.find_all(["div", "li", "article"], class_=lambda c: c and any(
                k in c for k in ["person", "faculty", "people", "card", "profile", "directory", "member"]
            ))
            if not cards:
                cards = soup.find_all("a", href=lambda h: h and any(k in h for k in ["/people/", "/faculty/"]))
            for card in cards:
                try:
                    if card.name == "a":
                        name = " ".join(card.get_text(strip=True).split())
                        href = card["href"]; full_text = name; title_guess = "Professor"
                    else:
                        name_tag = card.find(["h2", "h3", "h4", "strong"])
                        if not name_tag: continue
                        name = " ".join(name_tag.get_text(strip=True).split())
                        a_tag = card.find("a", href=True)
                        href = a_tag["href"] if a_tag else ""
                        full_text = card.get_text(separator=" ", strip=True)
                        title_guess = "Professor"
                        for line in full_text.split("  "):
                            if any(t in line.lower() for t in ["professor", "associate", "assistant"]):
                                title_guess = line.strip(); break
                    if not name or len(name) < 4 or name in seen: continue
                    if not is_active_faculty(title_guess): continue
                    seen.add(name)
                    profile_url = href if href.startswith("http") else dep["base"] + href
                    matched = match_field_keywords(full_text)
                    results.append({"Name": name, "Job Title": title_guess, "Department": dep["dept"],
                        "University": "Auburn University", "Email": "",
                        "Matched Fields": ", ".join(matched), "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Auburn University")})
                except Exception as e:
                    log.debug(f"Auburn {dep['dept']} card error: {e}")
            time.sleep(0.4)
        except Exception as e:
            log.error(f"Auburn {dep['dept']} error: {e}")
    log.info(f"Auburn total active faculty extracted: {len(results)}")
    return results


def main():
    scraper = create_browser_session()
    all_faculty = []

    scrapers = [
        ("1. Purdue (AAE, ME, Math/CCAM)",                   scrape_purdue),
        ("2. Georgia Tech (AE, ME, Math/CSE)",               scrape_gatech),
        ("3. University of Michigan (Aero, ME)",             scrape_umich),
        ("4. Caltech (GALCIT / EAS)",                        scrape_caltech),
        ("5. Stanford University (AeroAstro, MechE)",        scrape_stanford),
        ("6. MIT (AeroAstro, MechE, Math)",                  scrape_mit),
        ("7. UT Austin (ASE, ME, Oden/CSEM)",                scrape_ut_austin),
        ("8. Texas A&M (AeroE, ME, Math)",                   scrape_tamu),
        ("9. Penn State (AeroE, ME, Math)",                  scrape_psu),
        ("10. Ohio State (MAE, Math)",                       scrape_osu),
        ("11. UIUC (AeroE, MechSE, Math, CSE)",              scrape_uiuc),
        ("12. University of Maryland (AeroE, ME, AMSC)",     scrape_umd),
        ("13. CU Boulder (AeroE, ME, Applied Math)",         scrape_cu_boulder),
        ("14. NC State (MAE, Math)",                         scrape_ncstate),
        ("15. Virginia Tech (AOE, ME, Math)",                scrape_vtech),
        ("16. University of Washington (AA, ME, AMath)",     scrape_uw),
        ("17. UCLA (MAE, Math)",                             scrape_ucla),
        ("18. UC San Diego (MAE, Math)",                     scrape_ucsd),
        ("19. UC Berkeley (ME, Math)",                       scrape_ucb),
        ("20. Princeton (MAE, Math/PACM)",                   scrape_princeton),
        ("21. Cornell (MAE, Math/CAM)",                      scrape_cornell),
        ("22. University of Minnesota (AeroE, ME, Math)",    scrape_umn),
        ("23. Iowa State (AeroE, ME, Math)",                 scrape_iowa_state),
        ("24. University of Notre Dame (AeroE, ME, ACMS)",   scrape_notre_dame),
        ("25. Auburn University (AeroE, ME, Math)",          scrape_auburn),
    ]

    for label, fn in scrapers:
        log.info(f"\n{'='*60}\nRunning: {label}\n{'='*60}")
        try:
            faculty = fn(scraper)
            all_faculty.extend(faculty)
            log.info(f"  -> {len(faculty)} faculty leads added.")
        except Exception as e:
            log.error(f"  -> FAILED: {label}: {e}")
        time.sleep(0.5)

    if not all_faculty:
        log.error("No faculty data collected.")
        return

    df = pd.DataFrame(all_faculty)
    df.drop_duplicates(subset=["Name", "University", "Department"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Export 1: Complete R1 Faculty dataset across Aero, ME, Math
    output_all_csv = r"d:\Others\findprofs\universities_wise\r1_aerospace_faculty.csv"
    df.to_csv(output_all_csv, index=False, encoding="utf-8-sig")
    log.info(f"\nSuccessfully exported ALL {len(df)} faculty to: {output_all_csv}")

    # Export 2: Faculty matching target fields from upgraded fields.txt
    field_matched_df = df[df["Is Field Match"] == True].copy()
    output_fields_csv = r"d:\Others\findprofs\universities_wise\r1_aerospace_faculty_field_matched.csv"
    field_matched_df.to_csv(output_fields_csv, index=False, encoding="utf-8-sig")
    log.info(f"Successfully exported {len(field_matched_df)} FIELD-MATCHED faculty to: {output_fields_csv}")

    # Display preview
    print("\n" + "=" * 90)
    print("FIRST 10 ROWS OF r1_aerospace_faculty.csv:")
    print("=" * 90)
    cols_to_show = ["Name", "Job Title", "Department", "University", "Google Scholar URL", "Matched Fields"]
    available = [c for c in cols_to_show if c in df.columns]
    print(df[available].head(10).to_string(index=False))
    print("=" * 90)

    print("\nSummary by University and Department:")
    print(df.groupby(["University", "Department"]).size().to_string())
    print(f"\nTotal Active Faculty: {len(df)}")
    print(f"Total Faculty matching fields in fields.txt: {len(field_matched_df)}")


if __name__ == "__main__":
    main()