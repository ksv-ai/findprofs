"""
move_14_unis_to_others.py
=========================
Moves faculty from the 14 specified universities completely out of:
  - Master - All Live Verified
  - Aerospace Engineering
  - Mathematics & Comp Math
  - Mechanical Engineering

and appends them cleanly into:
  - Others University Faculties

Ensures formatting, freeze panes, autofilters, and column widths are refreshed.
"""

from copy import copy
from pathlib import Path
import openpyxl
from openpyxl.utils import get_column_letter

EXCEL_PATH = Path(r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx")

TARGET_UNIS = [
    "Baylor University",
    "Virginia Commonwealth University",
    "Case Western Reserve University",
    "Columbia University",
    "Georgia Institute of Technology",
    "Louisiana State University",
    "Northeastern University",
    "Northwestern University",
    "Old Dominion University",
    "Southern Illinois University Carbondale",
    "Southern Methodist University",
    "Stevens Institute of Technology",
    "University of California, Merced",
    "University of Denver",
]

TARGET_UNIS_LOWER = {u.strip().lower() for u in TARGET_UNIS}
OTHERS_TAB = "Others University Faculties"

FACULTY_SOURCE_SHEETS = [
    "Master - All Live Verified",
    "Aerospace Engineering",
    "Mathematics & Comp Math",
    "Mechanical Engineering",
]

def format_sheet_properly(ws):
    ws.freeze_panes = "A2"
    max_col_letter = get_column_letter(ws.max_column)
    ws.auto_filter.ref = f"A1:{max_col_letter}{ws.max_row}"

def main():
    print(f"Loading workbook: {EXCEL_PATH}")
    wb = openpyxl.load_workbook(EXCEL_PATH)

    master_ws = wb["Master - All Live Verified"]
    others_ws = wb[OTHERS_TAB]
    cols = master_ws.max_column

    # Existing keys in Others tab to avoid any duplicates: (clean_name, clean_uni)
    existing_others_keys = set()
    for r in range(2, others_ws.max_row + 1):
        name = str(others_ws.cell(r, 1).value or "").strip().lower()
        uni = str(others_ws.cell(r, 2).value or "").strip().lower()
        if name and uni:
            existing_others_keys.add((name, uni))

    print(f"Initial '{OTHERS_TAB}' faculty count: {others_ws.max_row - 1}")

    # 1. Extract rows from Master belonging to the 14 universities
    new_faculty_rows = []
    for r in range(2, master_ws.max_row + 1):
        uni = str(master_ws.cell(r, 2).value or "").strip().lower()
        if uni in TARGET_UNIS_LOWER:
            name = str(master_ws.cell(r, 1).value or "").strip().lower()
            key = (name, uni)
            if key not in existing_others_keys:
                existing_others_keys.add(key)
                row_data = []
                for c in range(1, cols + 1):
                    cell = master_ws.cell(r, c)
                    row_data.append((
                        cell.value,
                        copy(cell.fill),
                        copy(cell.font),
                        copy(cell.alignment),
                        cell.number_format
                    ))
                new_faculty_rows.append(row_data)

    print(f"Collected {len(new_faculty_rows)} faculty members to append to '{OTHERS_TAB}'")

    # 2. Append into 'Others University Faculties'
    current_others_row = others_ws.max_row + 1
    for row_vals in new_faculty_rows:
        for c_idx, (val, fill, font, align, num_fmt) in enumerate(row_vals, start=1):
            cell = others_ws.cell(current_others_row, c_idx)
            cell.value = val
            if fill: cell.fill = fill
            if font: cell.font = font
            if align: cell.alignment = align
            if num_fmt: cell.number_format = num_fmt
        current_others_row += 1

    print(f"New '{OTHERS_TAB}' faculty count: {others_ws.max_row - 1}")

    # 3. Delete rows matching the 14 universities from Master and Department tabs (bottom-up)
    for s_name in FACULTY_SOURCE_SHEETS:
        ws = wb[s_name]
        initial_cnt = ws.max_row - 1
        rows_to_delete = []
        for r in range(2, ws.max_row + 1):
            uni = str(ws.cell(r, 2).value or "").strip().lower()
            if uni in TARGET_UNIS_LOWER:
                rows_to_delete.append(r)

        for r in reversed(rows_to_delete):
            ws.delete_rows(r, 1)

        print(f"[{s_name}] Removed {len(rows_to_delete)} rows. Remaining faculty: {ws.max_row - 1}")

    # 4. Refresh formatting
    for s_name in FACULTY_SOURCE_SHEETS + [OTHERS_TAB]:
        format_sheet_properly(wb[s_name])

    # Save
    print("Saving workbook...")
    wb.save(EXCEL_PATH)
    print("[DONE] Successfully moved faculty from 14 universities to 'Others University Faculties'!")

if __name__ == "__main__":
    main()
