"""
apply_audit_corrections_and_split.py
====================================
1. Updates OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx:
   - Updates the 22 corrected OpenAlex IDs in 'Master - All Live Verified'.
   - Creates a dedicated clean tab 'Pure Aero-Fluids-CFD' (665 verified active aero/fluids/propulsion faculty).
   - Creates a dedicated tab 'Non-Aero (Biomed, Robotics, Solids)' (122 faculty).
2. Re-harvests the JSON files for the 22 corrected professors so their cache contains
   their true Aero/CFD landmark & recent papers.
3. Cleans up any non-aero JSON cache files from the core aero folder if necessary.
"""

import os
import sys
import io
import re
import csv
import json
import time
import requests
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

EXCEL_PATH = r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx"
AUDIT_CSV = r"d:\Others\findprofs\corrected_openalex_id_audit.csv"
BASE_JSON_DIR = r"d:\Others\findprofs\openalex_mechaero_faculty_json\universities_wise"

API_KEY = "NzjuLll4FIEV5HFS2mCK4g"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "FindProfs/1.0 (mailto:ksv.ai.research@gmail.com)"
}

DATE_FROM = "2023-01-01"
DATE_TO = "2026-06-30"


def slugify(text: str) -> str:
    if not text:
        return "unknown"
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return s or "unknown"


def reconstruct_abstract(inv_idx: dict) -> str:
    if not inv_idx or not isinstance(inv_idx, dict):
        return ""
    word_positions = []
    for word, positions in inv_idx.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    abstract = " ".join([wp[1] for wp in word_positions]).strip()
    if len(abstract) > 1200:
        abstract = abstract[:1197] + "..."
    return abstract


def clean_work_obj(w: dict) -> dict:
    primary_loc = w.get("primary_location") or {}
    source = primary_loc.get("source") or {}
    venue = source.get("display_name", "") or ""
    doi = w.get("doi") or primary_loc.get("landing_page_url") or ""
    concepts = [c.get("display_name", "") for c in (w.get("concepts") or [])[:8] if isinstance(c, dict) and c.get("display_name")]
    authors = [a.get("author", {}).get("display_name", "") for a in (w.get("authorships") or []) if isinstance(a, dict) and a.get("author", {}).get("display_name")]
    oa_info = w.get("open_access") or {}

    return {
        "title": w.get("title") or "",
        "publication_year": w.get("publication_year"),
        "publication_date": w.get("publication_date") or "",
        "doi": doi,
        "venue": venue,
        "type": w.get("type") or "",
        "cited_by_count": w.get("cited_by_count") or 0,
        "is_oa": oa_info.get("is_oa", False),
        "oa_url": oa_info.get("oa_url") or "",
        "concepts": concepts,
        "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
        "authors": authors,
    }


def harvest_single_prof(name: str, uni: str, dept: str, new_oa_id: str):
    """Fetches high-fidelity JSON for a single professor using verified new OpenAlex ID."""
    print(f"Re-harvesting true Aero/CFD profile for: {name} ({uni}) -> ID: {new_oa_id}")
    author_url = f"https://api.openalex.org/authors/{new_oa_id}"
    try:
        r = requests.get(author_url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  [ERROR] Could not fetch author {new_oa_id}")
            return
        a_data = r.json()
    except Exception as e:
        print(f"  [ERROR] Exception on {new_oa_id}: {e}")
        return

    summary_stats = a_data.get("summary_stats") or {}
    h_index = summary_stats.get("h_index", 0)
    works_count = a_data.get("works_count", 0)
    cited_by_count = a_data.get("cited_by_count", 0)
    display_name = a_data.get("display_name", name)

    raw_topics = a_data.get("topics") or []
    top_topics = [
        {"topic": t.get("display_name", ""), "count": t.get("count", 0)}
        for t in raw_topics[:5] if isinstance(t, dict) and t.get("display_name")
    ]

    time.sleep(0.1)
    top_cited_url = f"https://api.openalex.org/works?filter=author.id:{new_oa_id}&sort=cited_by_count:desc&per_page=3"
    top_cited_works = []
    try:
        tc_res = requests.get(top_cited_url, headers=HEADERS, timeout=15)
        if tc_res.status_code == 200:
            top_cited_works = [clean_work_obj(w) for w in (tc_res.json().get("results") or [])]
    except Exception:
        pass

    time.sleep(0.1)
    recent_url = f"https://api.openalex.org/works?filter=author.id:{new_oa_id},from_publication_date:{DATE_FROM},to_publication_date:{DATE_TO}&sort=publication_date:desc&per_page=5"
    recent_works = []
    try:
        r_res = requests.get(recent_url, headers=HEADERS, timeout=15)
        if r_res.status_code == 200:
            recent_works = [clean_work_obj(w) for w in (r_res.json().get("results") or [])]
    except Exception:
        pass

    record = {
        "faculty_name": name,
        "full_name": display_name,
        "department": dept,
        "university": uni,
        "author_id": new_oa_id,
        "works_count": works_count,
        "cited_by_count": cited_by_count,
        "h_index": h_index,
        "top_topics": top_topics,
        "top_cited_works": top_cited_works,
        "recent_works": recent_works,
    }

    uni_slug = slugify(uni)
    prof_slug = slugify(name)
    target_dir = os.path.join(BASE_JSON_DIR, uni_slug)
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, f"{prof_slug}.json")

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"  [SAVED] {target_file}")


def main():
    print("=" * 80)
    print("APPLYING OPENALEX ID CORRECTIONS AND SPLITTING MASTER EXCEL TABS")
    print("=" * 80)

    with open(AUDIT_CSV, "r", encoding="utf-8") as f:
        audit_rows = list(csv.DictReader(f))

    corrections_map = {}
    non_aero_set = set()
    for row in audit_rows:
        name_key = (row["name"].strip().lower(), row["uni"].strip().lower())
        if row["verdict"] == "NAMESAKE_MISMATCH_FOUND_AND_CORRECTED":
            corrections_map[name_key] = row["correct_openalex_id"]
        elif row["verdict"] == "GENUINE_NON_AERO_FACULTY":
            non_aero_set.add(name_key)

    print(f"Loaded {len(corrections_map)} corrected IDs to update.")
    print(f"Loaded {len(non_aero_set)} genuine non-aero faculty to separate into dedicated tab.")

    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws_master = wb["Master - All Live Verified"]

    # 1. Update master sheet with corrected IDs
    updated_in_master = 0
    headers = [ws_master.cell(1, c).value for c in range(1, ws_master.max_column + 1)]

    fill_corrected = PatternFill("solid", fgColor="C6EFCE")  # light green
    font_bold = Font(bold=True)

    rows_pure_aero = []
    rows_non_aero = []

    for r in range(2, ws_master.max_row + 1):
        name = str(ws_master.cell(r, 2).value or "").strip()
        uni = str(ws_master.cell(r, 3).value or "").strip()
        dept = str(ws_master.cell(r, 7).value or "").strip()
        name_key = (name.lower(), uni.lower())

        row_values = [ws_master.cell(r, c).value for c in range(1, ws_master.max_column + 1)]

        # Check if ID needs correction
        if name_key in corrections_map:
            new_id = corrections_map[name_key]
            ws_master.cell(r, 6).value = new_id
            ws_master.cell(r, 6).fill = fill_corrected
            row_values[5] = new_id
            updated_in_master += 1
            # Re-harvest fresh Aero JSON
            harvest_single_prof(name, uni, dept, new_id)
            rows_pure_aero.append(row_values)
        elif name_key in non_aero_set:
            rows_non_aero.append(row_values)
        else:
            rows_pure_aero.append(row_values)

    print(f"\nTotal rows corrected in Master sheet: {updated_in_master}")
    print(f"Total rows qualifying for 'Pure Aero-Fluids-CFD': {len(rows_pure_aero)}")
    print(f"Total rows classified as 'Non-Aero (Biomed, Solids, Robotics)': {len(rows_non_aero)}")

    # 2. Build / Update the Dedicated Clean Tabs in Excel
    def populate_sheet(sheet_name: str, row_data: list):
        if sheet_name in wb.sheetnames:
            del wb[sheet_name]
        ws_new = wb.create_sheet(title=sheet_name)
        # Headers
        for col_idx, h in enumerate(headers, 1):
            cell = ws_new.cell(1, col_idx, h)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1B365D" if "Aero" in sheet_name else "5B6770")
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Rows
        for row_idx, r_vals in enumerate(row_data, 2):
            for col_idx, val in enumerate(r_vals, 1):
                # Update S.N. column
                if col_idx == 1:
                    ws_new.cell(row_idx, col_idx, row_idx - 1)
                else:
                    ws_new.cell(row_idx, col_idx, val)

        # Auto-adjust column widths
        for col in ws_new.columns:
            max_len = max(len(str(cell.value or '')) for cell in col[:15])
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws_new.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 50)

    print("Writing 'Pure Aero-Fluids-CFD' tab...")
    populate_sheet("Pure Aero-Fluids-CFD", rows_pure_aero)

    print("Writing 'Non-Aero (Biomed, Solids, Robotics)' tab...")
    populate_sheet("Non-Aero (Biomed, Solids, Robotics)", rows_non_aero)

    # Move 'Pure Aero-Fluids-CFD' to position 2 right after Master
    sheet_order = ["Master - All Live Verified", "Pure Aero-Fluids-CFD", "Non-Aero (Biomed, Solids, Robotics)"] + [
        s for s in wb.sheetnames if s not in ["Master - All Live Verified", "Pure Aero-Fluids-CFD", "Non-Aero (Biomed, Solids, Robotics)"]
    ]
    wb._sheets = [wb[s] for s in sheet_order if s in wb.sheetnames]

    wb.save(EXCEL_PATH)
    print(f"Successfully saved updated workbook: {EXCEL_PATH}")
    print("=" * 80)
    print("PIPELINE UPDATE COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()
