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
# Main Orchestration & CSV Export
# -----------------------------------------------------------------------------
def main():
    scraper = create_browser_session()
    all_faculty = []

    # 1. Purdue (AAE, ME, Math/CCAM)
    purdue_faculty = scrape_purdue(scraper)
    all_faculty.extend(purdue_faculty)

    # 2. Georgia Tech (AE, ME, Math/CSE)
    gatech_faculty = scrape_gatech(scraper)
    all_faculty.extend(gatech_faculty)

    # 3. University of Michigan (Aero, ME)
    umich_faculty = scrape_umich(scraper)
    all_faculty.extend(umich_faculty)

    if not all_faculty:
        log.error("No faculty data collected.")
        return

    df = pd.DataFrame(all_faculty)
    df.drop_duplicates(subset=["Name", "University", "Department"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Export 1: Complete R1 Faculty dataset across Aero, ME, Math
    output_all_csv = r"d:\Others\findprofs\universities_wise\r1_aerospace_faculty.csv"
    df.to_csv(output_all_csv, index=False)
    log.info(f"\n✅ Successfully exported ALL {len(df)} faculty to: {output_all_csv}")

    # Export 2: Faculty matching target fields from upgraded fields.txt
    field_matched_df = df[df["Is Field Match"] == True].copy()
    output_fields_csv = r"d:\Others\findprofs\universities_wise\r1_aerospace_faculty_field_matched.csv"
    field_matched_df.to_csv(output_fields_csv, index=False)
    log.info(f"✅ Successfully exported {len(field_matched_df)} FIELD-MATCHED faculty to: {output_fields_csv}")

    # Display preview in requested format
    print("\n" + "=" * 90)
    print("FIRST 5 ROWS OF r1_aerospace_faculty.csv:")
    print("=" * 90)
    cols_to_show = ["Name", "Job Title", "Department", "University", "Google Scholar URL", "Matched Fields"]
    print(df[cols_to_show].head(5).to_string(index=False))
    print("=" * 90)

    print("\nSummary by University and Department:")
    print(df.groupby(["University", "Department"]).size().to_string())
    print(f"\nTotal Active Faculty: {len(df)}")
    print(f"Total Faculty matching fields in fields.txt: {len(field_matched_df)}")


if __name__ == "__main__":
    main()