"""
add_sn_column.py
================
Inserts 'S.N.' as the very first column (Column 1) across all sheets in:
  OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx

Numbers the rows 1, 2, 3, ... sequentially per sheet.
Preserves freeze panes (A2 or B2), formatting, autofilters, and column widths.
"""

from copy import copy
from pathlib import Path
import openpyxl
from openpyxl.utils import get_column_letter

EXCEL_PATH = Path(r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx")

def main():
    print(f"Loading workbook: {EXCEL_PATH}")
    wb = openpyxl.load_workbook(EXCEL_PATH)

    for s_name in wb.sheetnames:
        ws = wb[s_name]
        
        # Check if first column is already 'S.N.'
        first_val = str(ws.cell(1, 1).value or "").strip()
        if first_val in ["S.N.", "S.N", "SN", "Serial No", "Serial Number"]:
            print(f"[{s_name}] S.N. column already exists at Col 1. Re-numbering values...")
        else:
            print(f"[{s_name}] Inserting new S.N. column at Col 1...")
            ws.insert_cols(1)
            # Style header
            header_cell = ws.cell(1, 1)
            header_cell.value = "S.N."
            ref_header = ws.cell(1, 2)
            if ref_header.font: header_cell.font = copy(ref_header.font)
            if ref_header.fill: header_cell.fill = copy(ref_header.fill)
            if ref_header.border: header_cell.border = copy(ref_header.border)
            if ref_header.alignment: header_cell.alignment = copy(ref_header.alignment)

        # Number rows 1 to max_row-1
        for idx, r in enumerate(range(2, ws.max_row + 1), start=1):
            cell = ws.cell(r, 1)
            cell.value = idx
            cell.alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")
            # Copy border/font if adjacent cell has it
            ref_cell = ws.cell(r, 2)
            if ref_cell.font: cell.font = copy(ref_cell.font)
            if ref_cell.border: cell.border = copy(ref_cell.border)

        # Set width for S.N. column
        ws.column_dimensions["A"].width = 8

        # Set freeze pane so row 1 is frozen
        ws.freeze_panes = "B2" if s_name != "Target Category Breakdown" else "A2"

        # Update autofilter
        max_col_letter = get_column_letter(ws.max_column)
        ws.auto_filter.ref = f"A1:{max_col_letter}{ws.max_row}"

        print(f"  [{s_name}] Numbered {ws.max_row - 1} rows.")

    wb.save(EXCEL_PATH)
    print("\n[DONE] Successfully added and numbered S.N. column across all tabs!")

if __name__ == "__main__":
    main()
