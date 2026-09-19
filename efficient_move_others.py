"""
efficient_move_others.py
========================
Uses pandas to read/write cleanly and quickly, then applies styling using openpyxl.
"""

from copy import copy
from pathlib import Path
import openpyxl

EXCEL_PATH = Path(r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_CFD_AERO_COMPMATH.xlsx")

TARGET_UNIS = [
    "University of Alaska Fairbanks",
    "Naval Postgraduate School",
    "Portland State University",
    "Clarkson University",
    "Villanova University",
    "Western Michigan University",
    "University of Akron",
    "Cleveland State University",
    "South Dakota School of Mines and Technology",
    "New Mexico Tech",
    "University of New Orleans",
    "Marquette University",
    "Northern Illinois University",
    "Oakland University",
    "Louisiana Tech University",
    "University of South Alabama",
    "University of Texas Rio Grande Valley",
    "Georgia Southern University",
]
TARGET_UNIS_LOWER = {u.strip().lower() for u in TARGET_UNIS}
NEW_TAB_NAME = "Others University Faculties"

def main():
    print(f"Loading workbook: {EXCEL_PATH}")
    wb = openpyxl.load_workbook(EXCEL_PATH)

    faculty_sheets = [
        "Master - All Live Verified",
        "Aerospace Engineering",
        "Mathematics & Comp Math",
        "Mechanical Engineering",
    ]

    # 1. Collect faculty from Master for Others tab
    master_ws = wb["Master - All Live Verified"]
    cols = master_ws.max_column
    
    # Store headers (values and style prototypes)
    header_vals = [master_ws.cell(1, c).value for c in range(1, cols + 1)]
    header_styles = [
        {
            "font": copy(master_ws.cell(1, c).font),
            "fill": copy(master_ws.cell(1, c).fill),
            "border": copy(master_ws.cell(1, c).border),
            "alignment": copy(master_ws.cell(1, c).alignment),
        }
        for c in range(1, cols + 1)
    ]

    others_data = []
    for r in range(2, master_ws.max_row + 1):
        uni = str(master_ws.cell(r, 2).value or "").strip().lower()
        if uni in TARGET_UNIS_LOWER:
            row_vals = []
            for c in range(1, cols + 1):
                cell = master_ws.cell(r, c)
                row_vals.append((cell.value, copy(cell.fill), copy(cell.font), copy(cell.alignment), cell.number_format))
            others_data.append(row_vals)

    print(f"Found {len(others_data)} rows for '{NEW_TAB_NAME}'")

    # 2. Filter rows in each faculty sheet in reverse row order (fast delete_rows)
    for s_name in faculty_sheets:
        ws = wb[s_name]
        initial_rows = ws.max_row - 1
        rows_to_delete = []
        for r in range(2, ws.max_row + 1):
            uni = str(ws.cell(r, 2).value or "").strip().lower()
            if uni in TARGET_UNIS_LOWER:
                rows_to_delete.append(r)
        
        # Delete from bottom up
        for r in reversed(rows_to_delete):
            ws.delete_rows(r, 1)
            
        print(f"  [{s_name}] Deleted {len(rows_to_delete)} rows. Remaining: {ws.max_row - 1}")

    # 3. Create 'Others University Faculties' sheet
    if NEW_TAB_NAME in wb.sheetnames:
        del wb[NEW_TAB_NAME]
    others_ws = wb.create_sheet(title=NEW_TAB_NAME)

    # Write headers
    for c, val in enumerate(header_vals, start=1):
        cell = others_ws.cell(1, c)
        cell.value = val
        st = header_styles[c - 1]
        if st["font"]: cell.font = st["font"]
        if st["fill"]: cell.fill = st["fill"]
        if st["border"]: cell.border = st["border"]
        if st["alignment"]: cell.alignment = st["alignment"]

    # Write rows
    for r_idx, row_vals in enumerate(others_data, start=2):
        for c_idx, (val, fill, font, align, num_fmt) in enumerate(row_vals, start=1):
            cell = others_ws.cell(r_idx, c_idx)
            cell.value = val
            if fill: cell.fill = fill
            if font: cell.font = font
            if align: cell.alignment = align
            if num_fmt: cell.number_format = num_fmt

    # 4. Sheet ordering
    order = [
        "Master - All Live Verified",
        "Aerospace Engineering",
        "Mathematics & Comp Math",
        "Mechanical Engineering",
        NEW_TAB_NAME,
        "Target Category Breakdown",
    ]
    wb._sheets = [wb[s] for s in order if s in wb.sheetnames]

    # Save
    print("Saving workbook...")
    wb.save(EXCEL_PATH)
    print("[DONE] Successfully moved faculty to Others tab!")

if __name__ == "__main__":
    main()
