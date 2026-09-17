"""
R1 Aerospace Engineering Faculty Scraper & Field Filter
======================================================
Targets R1 Aerospace Engineering faculty directories:
  1. Purdue University (AAE)
  2. Georgia Tech (AE)
  3. University of Michigan (Aero)

Features:
  - Uses cloudscraper with browser emulation to bypass TLS fingerprinting and Cloudflare/WAFs.
  - Graceful fallback and per-card try/except blocks to prevent crashes.
  - Strict filtering of active faculty (excludes Emeritus, Adjunct, Staff, Lecturer).
  - Domain / Field matching against custom keywords defined in fields.txt.
  - Outputs full faculty dataset AND filtered field-specific faculty dataset to CSV.
"""

import os
import re
import time
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

# Keywords from fields.txt
TARGET_KEYWORDS = [
    "cfd", "computational fluid dynamics", "computational fluid mechanics",
    "computational aerodynamics", "aerodynamics", "fluid mechanics",
    "compressible flow", "high-speed flow", "hypersonics", "turbulence",
    "shock waves", "gas dynamics", "aerothermodynamics", "dns", "les", "turbulent flows",
    "rans", "numerical methods", "boundary-layer transition",
    "fluid-structure interaction", "aeroelasticity", "propulsion",
    "scramjets", "combustion", "reactive flows", "rarefied gas dynamics",
    "high-temperature flow", "aeroacoustics", "atmospheric entry", "uas", "uav", "drones",
    "spacecraft aerodynamics", "scientific computing", "computational physics",
    "numerical pdes", "multiphysics", "physics-informed ml", "pinn",
]

EXCLUDED_TITLES = ["emeritus", "adjunct", "staff", "lecturer", "postdoc", "visiting", "courtesy"]


def is_active_faculty(title: str) -> bool:
    """Return True if the title represents active faculty (not emeritus/adjunct/staff/lecturer)."""
    t_lower = title.lower()
    return not any(exc in t_lower for exc in EXCLUDED_TITLES)


def match_field_keywords(text: str) -> List[str]:
    """Find matching keywords from fields.txt inside text (case-insensitive with word boundaries)."""
    if not text:
        return []
    text_lower = text.lower()
    matches = []
    for kw in TARGET_KEYWORDS:
        # Match standalone words/phrases
        pattern = r"(?<!\w)" + re.escape(kw) + r"(?!\w)"
        if re.search(pattern, text_lower):
            matches.append(kw)
    return sorted(list(set(matches)))


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
# 1. Purdue University AAE Parser
# -----------------------------------------------------------------------------
def scrape_purdue(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Purdue School of Aeronautics and Astronautics faculty directory."""
    url = "https://engineering.purdue.edu/AAE/people/Faculty"
    log.info(f"Scraping Purdue: {url}")
    results = []

    try:
        resp = scraper.get(url, timeout=25)
        if resp.status_code != 200:
            log.error(f"Purdue HTTP {resp.status_code}")
            return results

        soup = BeautifulSoup(resp.text, "lxml")
        p_list = soup.find("div", class_="people-list")
        if not p_list:
            log.warning("Purdue people-list container not found")
            return results

        rows = p_list.find_all("div", class_="row", recursive=False)
        log.info(f"Found {len(rows)} faculty rows at Purdue")

        for row in rows:
            try:
                # Name
                name_col = row.find("div", class_="list-name")
                if not name_col:
                    continue
                name_a = name_col.find("a")
                name = name_a.get_text(separator=" ", strip=True) if name_a else name_col.get_text(separator=" ", strip=True)
                name = " ".join(name.split())
                if not name or len(name) < 3:
                    continue

                # Title & Info
                info_col = row.find("div", class_="list-info")
                if not info_col:
                    continue

                full_text = info_col.get_text(separator=" | ", strip=True)

                # The title in Purdue directory is in an unclassed <div> directly following list-name or inside it
                unclassed_divs = [d.get_text(strip=True) for d in name_col.find_all("div", recursive=False) if not d.get("class")]
                if not unclassed_divs:
                    unclassed_divs = [d.get_text(strip=True) for d in name_col.find_all("div") if not d.get("class")]
                
                title = "Professor"
                for u_text in unclassed_divs:
                    if u_text and not u_text.startswith("(") and not u_text.startswith("Ph.D.") and not u_text.startswith("Professor;"):
                        title = u_text
                        break
                if title == "Professor" and unclassed_divs:
                    title = unclassed_divs[0]

                # Filter active faculty
                if not is_active_faculty(title):
                    continue

                # Email
                email_a = info_col.find("a", href=re.compile(r"mailto:"))
                email = email_a["href"].replace("mailto:", "").strip() if email_a else ""

                # Extract matched keywords from bio/research text
                matched = match_field_keywords(full_text)

                results.append({
                    "Name": name,
                    "Job Title": title,
                    "University": "Purdue University",
                    "Email": email,
                    "Matched Fields": ", ".join(matched),
                    "Is Field Match": len(matched) > 0,
                    "Profile URL": f"https://engineering.purdue.edu{name_a['href']}" if name_a and name_a.get('href', '').startswith('/') else (name_a['href'] if name_a else ""),
                })
            except Exception as e:
                log.debug(f"Purdue card error: {e}")
                continue

    except Exception as e:
        log.error(f"Purdue scraper error: {e}")

    log.info(f"Extracted {len(results)} active faculty from Purdue")
    return results


# -----------------------------------------------------------------------------
# 2. Georgia Tech AE Parser
# -----------------------------------------------------------------------------
def scrape_gatech(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """Scrape Georgia Tech Guggenheim School of Aerospace Engineering faculty."""
    url = "https://ae.gatech.edu/academic-faculty-1"
    log.info(f"Scraping Georgia Tech: {url}")
    results = []

    try:
        resp = scraper.get(url, timeout=25)
        if resp.status_code != 200:
            log.warning(f"Georgia Tech {url} returned {resp.status_code}, falling back to /people")
            resp = scraper.get("https://ae.gatech.edu/people", timeout=25)

        if resp.status_code != 200:
            log.error(f"Georgia Tech returned HTTP {resp.status_code}")
            return results

        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.find_all(class_=re.compile(r"node--type-dir-person"))
        log.info(f"Found {len(cards)} faculty cards at Georgia Tech")

        for card in cards:
            try:
                # Name & Profile link
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

                # Job title
                title = "Professor"
                for p in parts:
                    if p != name and any(k in p.lower() for k in ["professor", "chair", "director", "engineer", "faculty"]):
                        title = p
                        break

                if not is_active_faculty(title):
                    continue

                # Email: can check profile or format
                email = ""
                profile_url = f"https://ae.gatech.edu{profile_path}" if profile_path.startswith("/") else profile_path
                
                # Fetch profile page to get email and detailed research bio
                matched = []
                if profile_url:
                    try:
                        time.sleep(0.3)
                        p_resp = scraper.get(profile_url, timeout=12)
                        if p_resp.status_code == 200:
                            p_soup = BeautifulSoup(p_resp.text, "lxml")
                            email_el = p_soup.find("a", href=re.compile(r"mailto:"))
                            if email_el:
                                email = email_el["href"].replace("mailto:", "").strip()
                            bio_text = p_soup.get_text(separator=" ", strip=True)
                            matched = match_field_keywords(bio_text)
                    except Exception:
                        pass

                if not matched:
                    matched = match_field_keywords(card_text)

                results.append({
                    "Name": name,
                    "Job Title": title,
                    "University": "Georgia Tech",
                    "Email": email,
                    "Matched Fields": ", ".join(matched),
                    "Is Field Match": len(matched) > 0,
                    "Profile URL": profile_url,
                })
            except Exception as e:
                log.debug(f"GaTech card error: {e}")
                continue

    except Exception as e:
        log.error(f"Georgia Tech scraper error: {e}")

    log.info(f"Extracted {len(results)} active faculty from Georgia Tech")
    return results


# -----------------------------------------------------------------------------
# 3. University of Michigan Aero Parser
# -----------------------------------------------------------------------------
def scrape_umich(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """
    Scrape University of Michigan Aerospace Engineering directory.
    Uses multi-page traversal with session warmup to bypass WAF.
    """
    base_url = "https://aero.engin.umich.edu/people/"
    log.info(f"Scraping University of Michigan: {base_url}")
    results = []

    try:
        # Warm up session on homepage
        scraper.get("https://aero.engin.umich.edu/", timeout=15)
        time.sleep(1)

        # Scrape through pages (pages 1 to 7)
        for page_num in range(1, 8):
            page_url = f"{base_url}?query-19-page={page_num}" if page_num > 1 else base_url
            log.info(f"Fetching UMich page {page_num}: {page_url}")

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
                log.warning(f"Could not load UMich page {page_num}")
                continue

            soup = BeautifulSoup(resp.text, "lxml")
            posts = soup.find_all(class_="wp-block-post")
            if not posts:
                log.info(f"No more posts found on page {page_num}")
                break

            for post in posts:
                try:
                    classes = post.get("class", [])

                    # Exclude staff, students, etc.
                    roles = [c.replace("role-", "") for c in classes if c.startswith("role-")]
                    if roles and not any("faculty" in r for r in roles):
                        continue

                    # Name
                    title_elem = post.find(class_="wp-block-post-title")
                    if not title_elem:
                        continue
                    name = title_elem.get_text(strip=True)
                    if not name:
                        continue

                    # Title / Position
                    p_texts = [p.get_text(strip=True) for p in post.find_all(["p", "div"]) if p.get_text(strip=True) and p.get_text(strip=True) != name]
                    job_title = p_texts[0] if p_texts else "Professor"

                    if not is_active_faculty(job_title):
                        continue

                    # Profile link
                    link_elem = title_elem.find("a") or post.find("a", href=True)
                    profile_url = link_elem["href"] if link_elem else ""

                    # Email
                    email_elem = post.find("a", href=re.compile(r"mailto:"))
                    email = email_elem["href"].replace("mailto:", "").strip() if email_elem else ""

                    # Research areas from classes and card text
                    research_tags = [c.replace("research-area-", "").replace("-", " ") for c in classes if c.startswith("research-area-")]
                    full_card_text = " ".join([name, job_title, " ".join(research_tags)] + p_texts)

                    matched = match_field_keywords(full_card_text)

                    results.append({
                        "Name": name,
                        "Job Title": job_title,
                        "University": "University of Michigan",
                        "Email": email,
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                    })
                except Exception as e:
                    log.debug(f"UMich post error: {e}")
                    continue

            time.sleep(0.5)

    except Exception as e:
        log.error(f"UMich scraper error: {e}")

    log.info(f"Extracted {len(results)} active faculty from University of Michigan")
    return results


# -----------------------------------------------------------------------------
# Main Execution & Export
# -----------------------------------------------------------------------------
def main():
    scraper = create_browser_session()
    all_faculty = []

    # 1. Purdue
    purdue_faculty = scrape_purdue(scraper)
    all_faculty.extend(purdue_faculty)

    # 2. Georgia Tech
    gatech_faculty = scrape_gatech(scraper)
    all_faculty.extend(gatech_faculty)

    # 3. University of Michigan
    umich_faculty = scrape_umich(scraper)
    all_faculty.extend(umich_faculty)

    if not all_faculty:
        log.error("No faculty data collected.")
        return

    df = pd.DataFrame(all_faculty)
    df.drop_duplicates(subset=["Name", "University"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Export 1: Complete R1 Aerospace Faculty dataset
    output_all_csv = r"d:\Others\findprofs\universities_wise\r1_aerospace_faculty.csv"
    df.to_csv(output_all_csv, index=False)
    log.info(f"\n✅ Successfully exported ALL {len(df)} faculty to: {output_all_csv}")

    # Export 2: Faculty matching target fields from fields.txt
    field_matched_df = df[df["Is Field Match"] == True].copy()
    output_fields_csv = r"d:\Others\findprofs\universities_wise\r1_aerospace_faculty_field_matched.csv"
    field_matched_df.to_csv(output_fields_csv, index=False)
    log.info(f"✅ Successfully exported {len(field_matched_df)} FIELD-MATCHED faculty to: {output_fields_csv}")

    # Display preview in requested format
    print("\n" + "=" * 80)
    print("FIRST 5 ROWS OF r1_aerospace_faculty.csv:")
    print("=" * 80)
    cols_to_show = ["Name", "Job Title", "University", "Email", "Matched Fields"]
    print(df[cols_to_show].head(5).to_string(index=False))
    print("=" * 80)

    print("\nSummary by University:")
    print(df["University"].value_counts().to_string())
    print(f"\nTotal Active Faculty: {len(df)}")
    print(f"Total Faculty matching fields in fields.txt: {len(field_matched_df)}")


if __name__ == "__main__":
    main()