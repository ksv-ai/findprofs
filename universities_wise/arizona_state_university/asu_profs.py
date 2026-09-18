import os
import sys
import re
import time
import logging
import urllib.parse
from typing import List, Dict

import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("asu_scraper")

# -----------------------------------------------------------------------------
# TARGET KEYWORDS & EXCLUDED TITLES
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
    """Filter out emeritus, adjunct, staff, postdocs, lecturers, etc."""
    if not title:
        return True
    t_lower = title.lower()
    return not any(exc in t_lower for exc in EXCLUDED_TITLES)


def match_field_keywords(text: str) -> List[str]:
    """Find matching keywords from fields ontology inside text."""
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


def get_google_scholar_url(name: str, university: str = "Arizona State University") -> str:
    """Generate direct Google Scholar search link."""
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
# ARIZONA STATE UNIVERSITY (SEMTE - Aerospace & Mechanical Engineering)
# -----------------------------------------------------------------------------
def scrape_asu(scraper: cloudscraper.CloudScraper) -> List[Dict]:
    """
    Scrape Arizona State University (ASU) SEMTE Aerospace & Mechanical Engineering faculty.
    Uses the underlying Search API powering:
    https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/
    """
    log.info("Scraping Arizona State University (SEMTE - Aerospace & Mechanical Engineering)...")
    results = []
    seen = set()

    # The directory page specifies dept_ids=1662 and an exclusion list for non-Aero/ME faculty
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
    page = 1
    total_pages = 1

    while page <= total_pages:
        params = {
            "dept_ids": "1662",
            "employee_types": "Faculty,Faculty w/Admin Appointment",
            "profiles_to_exclude": profiles_to_exclude,
            "size": "100",
            "page": str(page)
        }

        try:
            r = scraper.get(api_url, params=params, timeout=30)
            if r.status_code != 200:
                log.warning(f"ASU API returned status {r.status_code}")
                break

            data = r.json()
            total_pages = data.get("meta", {}).get("page", {}).get("total_pages", 1)
            raw_items = data.get("results", [])

            for item in raw_items:
                try:
                    name = item.get("display_name", {}).get("raw")
                    if not name:
                        first = item.get("first_name", {}).get("raw") or ""
                        last = item.get("last_name", {}).get("raw") or ""
                        name = f"{first} {last}".strip()

                    name = " ".join(name.split())
                    if not name or len(name) < 3 or name in seen:
                        continue

                    # Title detection
                    primary_titles = item.get("primary_title", {}).get("raw") or []
                    working_titles = item.get("working_title", {}).get("raw") or []
                    all_titles = item.get("titles", {}).get("raw") or []
                    home_rank = item.get("home_rank_description", {}).get("raw") or []

                    candidate_titles = []
                    for t_list in [primary_titles, working_titles, all_titles, home_rank]:
                        if isinstance(t_list, list):
                            candidate_titles.extend([t for t in t_list if t])
                        elif isinstance(t_list, str) and t_list:
                            candidate_titles.append(t_list)

                    title = "Professor"
                    for cand in candidate_titles:
                        cand_str = str(cand).strip()
                        if any(rk in cand_str.lower() for rk in ["professor", "assistant", "associate", "chair", "faculty"]):
                            title = cand_str
                            break

                    if not is_active_faculty(title):
                        continue

                    seen.add(name)

                    # Contact & Profile
                    email = item.get("email_address", {}).get("raw") or ""
                    asurite = item.get("asurite_id", {}).get("raw") or ""
                    profile_url = f"https://search.asu.edu/profile/{asurite}" if asurite else "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/"

                    # Text fields for keyword matching
                    text_parts = [name, title]
                    bio = item.get("bio", {}).get("raw") or ""
                    short_bio = item.get("short_bio", {}).get("raw") or ""
                    research_interests = item.get("research_interests", {}).get("raw") or ""
                    expertise_areas = item.get("expertise_areas", {}).get("raw") or []

                    # Clean HTML tags if present
                    if bio:
                        text_parts.append(BeautifulSoup(str(bio), "html.parser").get_text(separator=" "))
                    if short_bio:
                        text_parts.append(BeautifulSoup(str(short_bio), "html.parser").get_text(separator=" "))
                    if research_interests:
                        text_parts.append(BeautifulSoup(str(research_interests), "html.parser").get_text(separator=" "))
                    if isinstance(expertise_areas, list):
                        text_parts.extend(expertise_areas)

                    full_text = " | ".join(text_parts)
                    matched = match_field_keywords(full_text)

                    results.append({
                        "Name": name,
                        "Job Title": title,
                        "Department": "Aerospace & Mechanical Engineering",
                        "University": "Arizona State University",
                        "Email": email,
                        "Matched Fields": ", ".join(matched),
                        "Is Field Match": len(matched) > 0,
                        "Profile URL": profile_url,
                        "Google Scholar URL": get_google_scholar_url(name, "Arizona State University"),
                    })

                except Exception as e:
                    log.debug(f"Error parsing ASU faculty item: {e}")

            page += 1
            time.sleep(0.5)

        except Exception as e:
            log.error(f"Error fetching ASU faculty API page {page}: {e}")
            break

    log.info(f"ASU total active faculty extracted: {len(results)}")
    return results


def main():
    scraper = create_browser_session()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    log.info("=" * 60)
    log.info("Running Arizona State University Faculty Scraper")
    log.info("Source: https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/")
    log.info("=" * 60)

    faculty = scrape_asu(scraper)

    if not faculty:
        log.error("No faculty data collected.")
        return

    df = pd.DataFrame(faculty)
    df.drop_duplicates(subset=["Name", "University", "Department"], inplace=True)
    # Sort professors alphabetically from A to Z
    df.sort_values(by="Name", key=lambda col: col.str.strip().str.lower(), inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 1. Export ALL Active Faculty
    output_all_csv = os.path.join(script_dir, "asu_aerospace_mechanical_faculty.csv")
    df.to_csv(output_all_csv, index=False, encoding="utf-8-sig")
    log.info(f"\nSuccessfully exported ALL {len(df)} faculty (sorted A-Z) to: {output_all_csv}")

    # 2. Export Field-Matched Faculty
    field_matched_df = df[df["Is Field Match"] == True].copy()
    field_matched_df.sort_values(by="Name", key=lambda col: col.str.strip().str.lower(), inplace=True)
    field_matched_df.reset_index(drop=True, inplace=True)
    output_matched_csv = os.path.join(script_dir, "asu_aerospace_mechanical_faculty_field_matched.csv")
    field_matched_df.to_csv(output_matched_csv, index=False, encoding="utf-8-sig")
    log.info(f"Successfully exported {len(field_matched_df)} FIELD-MATCHED faculty (sorted A-Z) to: {output_matched_csv}")

    # 3. Export JSON & Excel with clickable hyperlinks
    output_json = os.path.join(script_dir, "asu_aerospace_mechanical_faculty.json")
    df.to_json(output_json, orient="records", indent=2)

    output_xlsx = os.path.join(script_dir, "asu_aerospace_mechanical_faculty.xlsx")
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

    sheets_data = [
        ("Field Matched Faculty (A-Z)", field_matched_df),
        ("All Active Faculty (A-Z)", df)
    ]

    for sheet_title, sheet_df in sheets_data:
        ws = wb.create_sheet(title=sheet_title)
        ws.views.sheetView[0].showGridLines = True
        headers = list(sheet_df.columns)
        ws.append(headers)

        for col_num in range(1, len(headers) + 1):
            c = ws.cell(row=1, column=col_num)
            c.font = header_font
            c.fill = header_fill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        prof_col_idx = headers.index("Profile URL") if "Profile URL" in headers else None
        scholar_col_idx = headers.index("Google Scholar URL") if "Google Scholar URL" in headers else None
        email_col_idx = headers.index("Email") if "Email" in headers else None

        for r_idx, row in sheet_df.iterrows():
            row_values = list(row)
            ws_row = r_idx + 2

            if prof_col_idx is not None:
                url = str(row_values[prof_col_idx])
                if url.startswith("http"):
                    row_values[prof_col_idx] = f'=HYPERLINK("{url}", "{url}")'

            if scholar_col_idx is not None:
                url = str(row_values[scholar_col_idx])
                if url.startswith("http"):
                    row_values[scholar_col_idx] = f'=HYPERLINK("{url}", "Google Scholar Profile")'

            if email_col_idx is not None:
                email = str(row_values[email_col_idx])
                if "@" in email:
                    row_values[email_col_idx] = f'=HYPERLINK("mailto:{email}", "{email}")'

            ws.append(row_values)

            for c_idx in range(1, len(headers) + 1):
                cell = ws.cell(row=ws_row, column=c_idx)
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center")

                if c_idx - 1 in [prof_col_idx, scholar_col_idx, email_col_idx]:
                    raw_v = str(sheet_df.iloc[r_idx, c_idx - 1])
                    if raw_v.startswith("http"):
                        cell.hyperlink = raw_v
                        cell.font = link_font
                    elif "@" in raw_v:
                        cell.hyperlink = f"mailto:{raw_v}"
                        cell.font = link_font

        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or '')
                if val.startswith('='):
                    l = 25 if 'Google Scholar Profile' in val else 40
                else:
                    l = len(val)
                if l > max_len:
                    max_len = l
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 65)

    wb.save(output_xlsx)
    log.info(f"Also exported JSON to {output_json} and clickable formatted Excel to {output_xlsx}")

    # Preview
    print("\n" + "=" * 90)
    print("FIRST 10 FIELD-MATCHED FACULTY AT ARIZONA STATE UNIVERSITY:")
    print("=" * 90)
    cols_to_show = ["Name", "Job Title", "Department", "Email", "Matched Fields", "Profile URL"]
    avail_cols = [c for c in cols_to_show if c in field_matched_df.columns]
    print(field_matched_df[avail_cols].head(10).to_string(index=False))
    print("=" * 90)

    print(f"\nTotal Active Faculty Extracted: {len(df)}")
    print(f"Total Faculty matching fields in fields.txt / TARGET_KEYWORDS: {len(field_matched_df)}")


if __name__ == "__main__":
    main()
