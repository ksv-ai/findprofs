import cloudscraper
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup
import re
import os
import sys
import time
import logging
import urllib.parse
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("asu_profs")

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

# Verified manual Google Scholar IDs (including Kang Ping Chen from user's screenshot)
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
    "Huan Wu": "8CS4X9IAAAAJ",
    "Jagannathan Rajagopalan": "ClqRIhIAAAAJ",
    "Jiefeng Sun": "fjUoHOsAAAAJ",
    "Konrad Rykaczewski": "SWeAf4UAAAAJ",
    "Minglei Qu": "9LWNC50AAAAJ",
    "Robert Wang": "LaUdx9gAAAAJ",
    "Spring Berman": "KKup0OgAAAAJ",
    "Wanxin Jin": "SoEC4h4AAAAJ",
    "Wonmo Kang": "bHyyOTAAAAAJ",
}


def is_active_faculty(title: str) -> bool:
    if not title:
        return True
    t_lower = title.lower()
    return not any(exc in t_lower for exc in EXCLUDED_TITLES)


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


def scrape_asu(scraper: cloudscraper.CloudScraper) -> List[Dict]:
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

                # Title resolution
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

                email = item.get("email_address", {}).get("raw") or ""
                asurite = item.get("asurite_id", {}).get("raw") or ""
                profile_url = f"https://search.asu.edu/profile/{asurite}" if asurite else "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/"

                # Build text for field matching
                text_parts = [name, title]
                bio = item.get("bio", {}).get("raw") or ""
                short_bio = item.get("short_bio", {}).get("raw") or ""
                research_interests = item.get("research_interests", {}).get("raw") or ""
                expertise_areas = item.get("expertise_areas", {}).get("raw") or []

                clean_bio = " ".join(BeautifulSoup(str(bio), "html.parser").get_text(separator=" ").split()) if bio else ""
                clean_short_bio = " ".join(BeautifulSoup(str(short_bio), "html.parser").get_text(separator=" ").split()) if short_bio else ""
                clean_interests = " ".join(BeautifulSoup(str(research_interests), "html.parser").get_text(separator=" ").split()) if research_interests else ""
                expertise_str = ", ".join(expertise_areas) if isinstance(expertise_areas, list) else str(expertise_areas)

                # Combined biography summary
                bio_summary = clean_short_bio if clean_short_bio else clean_bio
                if len(bio_summary) > 400:
                    bio_summary = bio_summary[:397] + "..."

                if clean_bio:
                    text_parts.append(clean_bio)
                if clean_short_bio:
                    text_parts.append(clean_short_bio)
                if clean_interests:
                    text_parts.append(clean_interests)
                if expertise_str:
                    text_parts.append(expertise_str)

                full_text = " | ".join(text_parts)
                matched = match_field_keywords(full_text)

                # Scholar ID detection
                scholar_id = KNOWN_SCHOLAR_IDS.get(name, "")

                results.append({
                    "Name": name,
                    "Job Title": title,
                    "Department": "Aerospace & Mechanical Engineering",
                    "University": "Arizona State University",
                    "Email": email,
                    "Matched Count": len(matched),
                    "Matched Fields": ", ".join(matched),
                    "Research Interests": clean_interests if clean_interests else expertise_str,
                    "Expertise Areas": expertise_str,
                    "Research / Bio Summary": bio_summary,
                    "Is Field Match": len(matched) > 0,
                    "Scholar ID": scholar_id,
                    "Profile URL": profile_url,
                    "Google Scholar URL": "",  # will be generated
                    "Directory URL": "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/",
                    "asurite": asurite
                })

            except Exception as e:
                log.debug(f"Error parsing ASU faculty item: {e}")

    except Exception as e:
        log.error(f"Error calling ASU API: {e}")

    # Second pass: check profile pages of those without scholar_id
    log.info(f"Checking profile pages to extract direct Scholar User IDs...")
    for prof in results:
        if not prof["Scholar ID"] and prof["asurite"]:
            try:
                p_url = f"https://search.asu.edu/profile/{prof['asurite']}"
                r_prof = scraper.get(p_url, timeout=10)
                if r_prof.status_code == 200:
                    m = re.findall(r'user=([a-zA-Z0-9_-]{12})', r_prof.text)
                    if m:
                        prof["Scholar ID"] = m[0]
            except Exception:
                pass
            time.sleep(0.15)

        prof["Google Scholar URL"] = build_scholar_url(prof["Name"], prof["Scholar ID"])

    # Sort primarily by Matched Count (descending: max matched first), then by Name (A-Z)
    results.sort(key=lambda x: (-x["Matched Count"], x["Name"].strip().lower()))
    log.info(f"Total active faculty extracted: {len(results)}")
    return results


def export_to_excel(faculty_list: List[Dict], output_path: str):
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

    field_matched_list = [f for f in faculty_list if f["Is Field Match"]]
    # Ensure field matched is sorted by maximum matched keywords first
    field_matched_list.sort(key=lambda x: (-x["Matched Count"], x["Name"].strip().lower()))

    columns_to_export = [
        "Name", "Job Title", "Department", "University", "Email",
        "Matched Count", "Matched Fields", "Research Interests", "Expertise Areas",
        "Research / Bio Summary", "Is Field Match", "Scholar ID", "Profile URL",
        "Google Scholar URL", "Directory URL"
    ]

    sheets_data = [
        ("Field Matched (Max Keywords)", field_matched_list),
        ("All Faculty (Max Keywords)", faculty_list)
    ]

    for sheet_title, data_rows in sheets_data:
        ws = wb.create_sheet(title=sheet_title)
        ws.views.sheetView[0].showGridLines = True
        ws.append(columns_to_export)

        # Style header
        for col_num in range(1, len(columns_to_export) + 1):
            c = ws.cell(row=1, column=col_num)
            c.font = header_font
            c.fill = header_fill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        prof_col_idx = columns_to_export.index("Profile URL")
        scholar_col_idx = columns_to_export.index("Google Scholar URL")
        email_col_idx = columns_to_export.index("Email")
        dir_col_idx = columns_to_export.index("Directory URL")

        for r_idx, row_dict in enumerate(data_rows):
            row_values = [row_dict.get(c, "") for c in columns_to_export]
            ws_row = r_idx + 2

            # Set HYPERLINK formulas
            p_url = row_dict.get("Profile URL", "")
            s_url = row_dict.get("Google Scholar URL", "")
            email = row_dict.get("Email", "")
            s_id = row_dict.get("Scholar ID", "")
            d_url = row_dict.get("Directory URL", "")

            if p_url.startswith("http"):
                row_values[prof_col_idx] = f'=HYPERLINK("{p_url}", "{p_url}")'

            if s_url.startswith("http"):
                label = f"Scholar ({s_id})" if s_id else "Google Scholar Search"
                row_values[scholar_col_idx] = f'=HYPERLINK("{s_url}", "{label}")'

            if email and "@" in email:
                row_values[email_col_idx] = f'=HYPERLINK("mailto:{email}", "{email}")'

            if d_url.startswith("http"):
                row_values[dir_col_idx] = f'=HYPERLINK("{d_url}", "{d_url}")'

            ws.append(row_values)

            # Apply cell styles and openpyxl hyperlink objects
            for c_idx in range(1, len(columns_to_export) + 1):
                cell = ws.cell(row=ws_row, column=c_idx)
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center")

                if c_idx - 1 == prof_col_idx and p_url.startswith("http"):
                    cell.hyperlink = p_url
                    cell.font = link_font
                elif c_idx - 1 == scholar_col_idx and s_url.startswith("http"):
                    cell.hyperlink = s_url
                    cell.font = link_font
                elif c_idx - 1 == email_col_idx and "@" in email:
                    cell.hyperlink = f"mailto:{email}"
                    cell.font = link_font
                elif c_idx - 1 == dir_col_idx and d_url.startswith("http"):
                    cell.hyperlink = d_url
                    cell.font = link_font

        # Auto-fit column widths
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

    # 1. Remove CSV files as requested
    for f in os.listdir(script_dir):
        if f.endswith(".csv") or f.endswith(".json"):
            csv_f = os.path.join(script_dir, f)
            try:
                os.remove(csv_f)
                log.info(f"Removed unnecessary file: {f}")
            except Exception as e:
                log.warning(f"Could not remove {f}: {e}")

    # 2. Scrape and generate faculty records
    faculty = scrape_asu(scraper)

    # 3. Export exclusively to formatted Excel (.xlsx)
    excel_path = os.path.join(script_dir, "asu_aerospace_mechanical_faculty.xlsx")
    export_to_excel(faculty, excel_path)

    # 4. Preview
    matched_count = sum(1 for f in faculty if f["Is Field Match"])
    with_id_count = sum(1 for f in faculty if f["Scholar ID"])

    print("\n" + "=" * 95)
    print("ASU FACULTY SCRAPING COMPLETED (ONLY EXCEL GENERATED)")
    print("=" * 95)
    print(f"Total Active Faculty (A-Z): {len(faculty)}")
    print(f"Field-Matched Faculty: {matched_count}")
    print(f"Direct Google Scholar User IDs embedded: {with_id_count}")
    print(f"Excel Workbook Path: {excel_path}")
    print("=" * 95)


if __name__ == "__main__":
    main()
