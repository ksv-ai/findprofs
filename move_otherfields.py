"""
move_otherfields.py
===================
1. Moves all faculty with Primary Target Category:
   '10. Multiphysics & Thermal-Fluid Sciences'
   from:
     - Master - All Live Verified
     - Aerospace Engineering
     - Mathematics & Comp Math
     - Mechanical Engineering
     - Others University Faculties
   into a new dedicated tab:
     - otherfields

2. Formats all tables properly:
   - Freezes the top header row (freeze panes at row 2)
   - Auto-adjusts column widths dynamically with padding so text isn't clipped
   - Enables AutoFilter on header row
   - Clean professional styling across all sheets
"""

from copy import copy
from pathlib import Path
import openpyxl
from openpyxl.utils import get_column_letter

EXCEL_PATH = Path(r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_CFD_AERO_COMPMATH.xlsx")
NEW_TAB_NAME = "otherfields"
TARGET_CAT = "10. Multiphysics & Thermal-Fluid Sciences"

FACULTY_SHEETS = [
    "Master - All Live Verified",
    "Aerospace Engineering",
    "Mathematics & Comp Math",
    "Mechanical Engineering",
    "Others University Faculties",
]

def format_sheet_properly(ws):
    """Applies clean table formatting: freeze pane, auto column width, autofilter."""
    # Freeze top row
    ws.freeze_panes = "A2"
    
    # AutoFilter
    max_col_letter = get_column_letter(ws.max_column)
    ws.auto_filter.ref = f"A1:{max_col_letter}{ws.max_row}"

    # Auto-adjust column widths with bounds
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        header_val = str(col[0].value or "")
        
        # Sample top 60 rows for speed and good approximation
        sample_rows = col[:60]
        for cell in sample_rows:
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        
        # Specific column width logic based on header name
        if "Research Focus" in header_val:
            ws.column_dimensions[col_letter].width = 50
        elif "Name" == header_val:
            ws.column_dimensions[col_letter].width = 28
        elif "University" == header_val:
            ws.column_dimensions[col_letter].width = 34
        elif "OpenAlex ID" in header_val:
            ws.column_dimensions[col_letter].width = 16
        elif "Category" in header_val:
            ws.column_dimensions[col_letter].width = 36
        elif "Department" in header_val:
            ws.column_dimensions[col_letter].width = 38
        elif "Email" in header_val:
            ws.column_dimensions[col_letter].width = 32
        elif "URL" in header_val:
            ws.column_dimensions[col_letter].width = 35
        else:
            calc_width = max(max_len + 3, len(header_val) + 4)
            ws.column_dimensions[col_letter].width = min(max(calc_width, 14), 50)


def main():
    print(f"Loading workbook: {EXCEL_PATH}")
    wb = openpyxl.load_workbook(EXCEL_PATH)

    master_ws = wb["Master - All Live Verified"]
    cols = master_ws.max_column

    # Header values & style prototype
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

    # Find category column index (1-based)
    cat_col = header_vals.index("Primary Target Category") + 1
    print(f"Category column is at index {cat_col} ('{header_vals[cat_col - 1]}')")

    # 1. Extract matching professors from Master for 'otherfields'
    otherfields_rows = []
    for r in range(2, master_ws.max_row + 1):
        cat_val = str(master_ws.cell(r, cat_col).value or "").strip()
        if cat_val == TARGET_CAT or "10." in cat_val:
            row_data = []
            for c in range(1, cols + 1):
                cell = master_ws.cell(r, c)
                row_data.append((cell.value, copy(cell.fill), copy(cell.font), copy(cell.alignment), cell.number_format))
            otherfields_rows.append(row_data)

    print(f"Collected {len(otherfields_rows)} professors for '{NEW_TAB_NAME}' tab.")

    # 2. Delete matching rows from each faculty sheet (bottom-up)
    for s_name in FACULTY_SHEETS:
        if s_name not in wb.sheetnames:
            continue
        ws = wb[s_name]
        c_idx = cat_col
        # Verify category col for this sheet
        for c in range(1, ws.max_column + 1):
            if ws.cell(1, c).value == "Primary Target Category":
                c_idx = c
                break
        
        rows_to_delete = []
        for r in range(2, ws.max_row + 1):
            cat_val = str(ws.cell(r, c_idx).value or "").strip()
            if cat_val == TARGET_CAT or "10." in cat_val:
                rows_to_delete.append(r)

        for r in reversed(rows_to_delete):
            ws.delete_rows(r, 1)

        print(f"  [{s_name}] Deleted {len(rows_to_delete)} rows. Remaining faculty: {ws.max_row - 1}")

    # 3. Create 'otherfields' sheet
    if NEW_TAB_NAME in wb.sheetnames:
        del wb[NEW_TAB_NAME]
    otherfields_ws = wb.create_sheet(title=NEW_TAB_NAME)

    # Write headers
    for c, val in enumerate(header_vals, start=1):
        cell = otherfields_ws.cell(1, c)
        cell.value = val
        st = header_styles[c - 1]
        if st["font"]: cell.font = st["font"]
        if st["fill"]: cell.fill = st["fill"]
        if st["border"]: cell.border = st["border"]
        if st["alignment"]: cell.alignment = st["alignment"]

    # Write data rows
    for r_idx, row_vals in enumerate(otherfields_rows, start=2):
        for c_idx, (val, fill, font, align, num_fmt) in enumerate(row_vals, start=1):
            cell = otherfields_ws.cell(r_idx, c_idx)
            cell.value = val
            if fill: cell.fill = fill
            if font: cell.font = font
            if align: cell.alignment = align
            if num_fmt: cell.number_format = num_fmt

    # 4. Clean trailing empty rows across sheets
    all_faculty_sheets = FACULTY_SHEETS + [NEW_TAB_NAME]
    for s_name in all_faculty_sheets:
        ws = wb[s_name]
        valid_rows = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value is not None]
        if len(valid_rows) < ws.max_row:
            print(f"Trimming {ws.max_row - len(valid_rows)} blank trailing rows in {s_name}...")
            data = []
            for r in valid_rows:
                row_vals = []
                for c in range(1, ws.max_column + 1):
                    cell = ws.cell(r, c)
                    row_vals.append((cell.value, copy(cell.fill), copy(cell.font), copy(cell.alignment), cell.number_format))
                data.append(row_vals)
            
            idx = wb.sheetnames.index(s_name)
            del wb[s_name]
            clean_ws = wb.create_sheet(title=s_name, index=idx)
            for r_idx, row_vals in enumerate(data, start=1):
                for c_idx, (val, fill, font, align, num_fmt) in enumerate(row_vals, start=1):
                    cell = clean_ws.cell(r_idx, c_idx)
                    cell.value = val
                    if fill: cell.fill = fill
                    if font: cell.font = font
                    if align: cell.alignment = align
                    if num_fmt: cell.number_format = num_fmt

    # 5. Format all tables properly
    print("\n--- Formatting All Sheets Properly ---")
    for s_name in wb.sheetnames:
        if s_name != "Target Category Breakdown":
            print(f"  Formatting sheet: {s_name}")
            format_sheet_properly(wb[s_name])
        else:
            wb[s_name].freeze_panes = "A2"

    # 6. Sheet ordering
    desired_order = [
        "Master - All Live Verified",
        "Aerospace Engineering",
        "Mathematics & Comp Math",
        "Mechanical Engineering",
        "Others University Faculties",
        NEW_TAB_NAME,
        "Target Category Breakdown",
    ]
    wb._sheets = [wb[s] for s in desired_order if s in wb.sheetnames]

    # Save workbook
    print("\nSaving workbook...")
    wb.save(EXCEL_PATH)
    print("[DONE] Successfully moved category 10 faculty to 'otherfields' and formatted all tables!")

if __name__ == "__main__":
    main()
