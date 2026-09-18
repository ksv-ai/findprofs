import os
import re
import time
import logging
import urllib.parse
from typing import List, Dict

import cloudscraper
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("asu_scraper")

# Comprehensive research keywords from fields.txt and user instructions
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

# Strict exclusions for inactive, emeritus, retired, or non-regular faculty
EXCLUDED_KEYWORDS = [
    "emeritus", "retired", "adjunct", "visiting", "lecturer", "staff",
    "postdoc", "courtesy", "administrative", "coordinator", "advisor",
    "manager", "instructor", "emerita"
]

# Verified manual Google Scholar IDs
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


def is_active_faculty(item: Dict) -> bool:
    """
    Strict active faculty filter:
    Inspects ALL titles, affiliations, subaffiliations, and department records.
    Immediately rejects any faculty member with emeritus, retired, adjunct,
    visiting, lecturer, instructor, postdoc, or staff designations.
    """
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
    """Resolves the most appropriate academic faculty title."""
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
            # Clean up unwanted suffixes if any
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
        log.info(f"Retrieved {len(raw_items)} raw items from ASU API.")

        for item in raw_items:
            try:
                # 1. STRICT ACTIVE FACULTY FILTER (removes emeritus, retired, adjunct, etc.)
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

                # 3. Lab / Personal Website extraction
                res_web = item.get("research_website", {}).get("raw") or ""
                gen_web = item.get("website", {}).get("raw") or ""
                lab_website = res_web or gen_web or ""

                # 4. Text for field matching & research profiles
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

                full_text = " | ".join(text_parts)
                matched = match_field_keywords(full_text)

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
                    "Education / Degrees": clean_edu,
                    "Office Location": "",  # To be enriched from profile page
                    "Lab / Personal Website": lab_website,
                    "Is Field Match": len(matched) > 0,
                    "Scholar ID": scholar_id,
                    "Profile URL": profile_url,
                    "Google Scholar URL": "",  # To be generated
                    "Directory URL": "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/",
                    "asurite": asurite
                })

            except Exception as e:
                log.debug(f"Error parsing ASU faculty item: {e}")

    except Exception as e:
        log.error(f"Error calling ASU API: {e}")

    # Second pass: Enrich profile pages for office locations & Google Scholar IDs
    log.info(f"Enriching {len(results)} active faculty profiles with office locations and Google Scholar IDs...")
    for idx, prof in enumerate(results):
        if prof["asurite"]:
            try:
                p_url = f"https://search.asu.edu/profile/{prof['asurite']}"
                r_prof = scraper.get(p_url, timeout=12)
                if r_prof.status_code == 200:
                    # Scholar ID extraction
                    if not prof["Scholar ID"]:
                        m = re.findall(r'user=([a-zA-Z0-9_-]{12})', r_prof.text)
                        if m:
                            prof["Scholar ID"] = m[0]

                    # Office location extraction
                    soup_prof = BeautifulSoup(r_prof.text, "html.parser")
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

        prof["Google Scholar URL"] = build_scholar_url(prof["Name"], prof["Scholar ID"])

    # Sort primarily by Matched Count (descending: max keywords matched first), then by Name (A-Z)
    results.sort(key=lambda x: (-x["Matched Count"], x["Name"].strip().lower()))
    log.info(f"Total active faculty successfully extracted: {len(results)}")
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

    # Filter matched list - strict active faculty only (no emeritus/retired)
    field_matched_list = [f for f in faculty_list if f["Is Field Match"]]
    field_matched_list.sort(key=lambda x: (-x["Matched Count"], x["Name"].strip().lower()))

    # Complete columns requested by user
    columns_to_export = [
        "Name", "Job Title", "Department", "University", "Email",
        "Matched Count", "Matched Fields", "Research Interests", "Expertise Areas",
        "Research / Bio Summary", "Education / Degrees", "Office Location",
        "Lab / Personal Website", "Is Field Match", "Scholar ID", "Profile URL",
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
        web_col_idx = columns_to_export.index("Lab / Personal Website")
        dir_col_idx = columns_to_export.index("Directory URL")

        for r_idx, row_dict in enumerate(data_rows):
            row_values = [row_dict.get(c, "") for c in columns_to_export]
            ws_row = r_idx + 2

            p_url = row_dict.get("Profile URL", "")
            s_url = row_dict.get("Google Scholar URL", "")
            email = row_dict.get("Email", "")
            s_id = row_dict.get("Scholar ID", "")
            lab_web = row_dict.get("Lab / Personal Website", "")
            d_url = row_dict.get("Directory URL", "")

            # Active clickable hyperlink formulas
            if p_url.startswith("http"):
                row_values[prof_col_idx] = f'=HYPERLINK("{p_url}", "{p_url}")'

            if s_url.startswith("http"):
                label = f"Scholar ({s_id})" if s_id else "Google Scholar Search"
                row_values[scholar_col_idx] = f'=HYPERLINK("{s_url}", "{label}")'

            if email and "@" in email:
                row_values[email_col_idx] = f'=HYPERLINK("mailto:{email}", "{email}")'

            if lab_web.startswith("http"):
                row_values[web_col_idx] = f'=HYPERLINK("{lab_web}", "{lab_web}")'

            if d_url.startswith("http"):
                row_values[dir_col_idx] = f'=HYPERLINK("{d_url}", "{d_url}")'

            ws.append(row_values)

            # Apply openpyxl hyperlink objects & cell styling
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
                elif c_idx - 1 == web_col_idx and lab_web.startswith("http"):
                    cell.hyperlink = lab_web
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

    # 1. Clean up any CSV/JSON files as strictly required
    for f in os.listdir(script_dir):
        if f.endswith(".csv") or f.endswith(".json"):
            csv_f = os.path.join(script_dir, f)
            try:
                os.remove(csv_f)
                log.info(f"Removed unnecessary file: {f}")
            except Exception as e:
                log.warning(f"Could not remove {f}: {e}")

    # 2. Scrape and generate active faculty records
    faculty = scrape_asu(scraper)

    # 3. Export exclusively to formatted Excel (.xlsx)
    excel_path = os.path.join(script_dir, "asu_aerospace_mechanical_faculty.xlsx")
    export_to_excel(faculty, excel_path)

    # 4. Preview summary
    matched_count = sum(1 for f in faculty if f["Is Field Match"])
    with_id_count = sum(1 for f in faculty if f["Scholar ID"])
    with_edu_count = sum(1 for f in faculty if f["Education / Degrees"])
    with_office_count = sum(1 for f in faculty if f["Office Location"])
    with_web_count = sum(1 for f in faculty if f["Lab / Personal Website"])

    print("\n" + "=" * 95)
    print("ASU FACULTY SCRAPING COMPLETED (ONLY EXCEL WORKBOOK GENERATED)")
    print("=" * 95)
    print(f"Total Active Faculty (sorted by max keywords matched): {len(faculty)}")
    print(f"Field-Matched Faculty: {matched_count}")
    print(f"Direct Google Scholar User IDs: {with_id_count}")
    print(f"Faculty with Education / Degrees scraped: {with_edu_count}")
    print(f"Faculty with Office Location scraped: {with_office_count}")
    print(f"Faculty with Lab / Personal Website scraped: {with_web_count}")
    print(f"Excel Workbook Path: {excel_path}")
    print("=" * 95)


if __name__ == "__main__":
    main()
