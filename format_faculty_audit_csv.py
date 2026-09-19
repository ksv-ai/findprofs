"""
format_faculty_audit_csv.py
===========================
1. Ensures faculty_status_audit.csv is strictly ordered by S.N. from smallest (1) to largest (1269).
2. Converts the 'Profile URL' column into clickable direct hyperlink formulas: =HYPERLINK("...", "...")
   so when opened in Excel or spreadsheet viewers, it is clickable directly with a single click.
3. Also generates an accompanying 'faculty_status_audit.xlsx' with native styled clickable blue hyperlinks.
"""

import csv
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

CSV_PATH = Path(r"d:\Others\findprofs\faculty_status_audit.csv")
XLSX_PATH = Path(r"d:\Others\findprofs\faculty_status_audit.xlsx")

def main():
    print(f"Reading: {CSV_PATH}")
    with open(CSV_PATH, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # 1. Sort strictly by S.N. ascending (smallest to largest)
    rows.sort(key=lambda r: int(r[0]) if r[0].strip().isdigit() else 999999)
    print(f"Sorted {len(rows)} rows by S.N. (from {rows[0][0]} to {rows[-1][0]}).")

    # 2. Write back to CSV with Excel-compatible =HYPERLINK("...", "...") formulas for direct clickability
    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            url = r[-1].strip()
            # If valid URL, format as clickable hyperlink formula
            if url.startswith("http"):
                r_formatted = r[:-1] + [f'=HYPERLINK("{url}","{url}")']
            else:
                r_formatted = r
            writer.writerow(r_formatted)

    print(f"[DONE] Formatted CSV saved: {CSV_PATH}")

    # 3. Also generate a beautifully styled .xlsx version with native clickable hyperlinks
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Faculty Status Audit"

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    link_font = Font(name="Calibri", size=10, color="0000FF", underline="single")
    regular_font = Font(name="Calibri", size=10)
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )

    # Write headers
    for c_idx, h in enumerate(header, start=1):
        cell = ws.cell(1, c_idx, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Action color fills
    fill_keep = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")     # Light green
    fill_remove = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")   # Light red/peach
    fill_review = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")   # Light yellow

    # Write data
    for r_idx, r in enumerate(rows, start=2):
        action_text = r[8] # Recommended Action
        row_fill = None
        if "KEEP" in action_text:
            row_fill = fill_keep
        elif "REMOVE" in action_text:
            row_fill = fill_remove
        elif "REVIEW" in action_text:
            row_fill = fill_review

        for c_idx, val in enumerate(r, start=1):
            cell = ws.cell(r_idx, c_idx)
            cell.font = regular_font
            cell.border = thin_border
            if row_fill:
                cell.fill = row_fill

            # Column 1 (S.N.) - integer format
            if c_idx == 1:
                cell.value = int(val) if val.isdigit() else val
                cell.alignment = center_align
            # Column 8 (Papers count) - integer format
            elif c_idx == 8:
                cell.value = int(val) if str(val).isdigit() else val
                cell.alignment = center_align
            # Column 10 (Profile URL) - native clickable hyperlink
            elif c_idx == 10:
                url = str(val).strip()
                cell.value = url
                if url.startswith("http"):
                    cell.hyperlink = url
                    cell.font = link_font
                cell.alignment = left_align
            else:
                cell.value = val
                cell.alignment = center_align if c_idx in [4, 6, 7] else left_align

    # Freeze panes at A2
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(header))}{len(rows)+1}"

    # Auto-adjust column widths
    widths = {
        "A": 8,   # S.N.
        "B": 28,  # Name
        "C": 34,  # University
        "D": 16,  # OpenAlex ID
        "E": 24,  # Detected Title
        "F": 22,  # Web Status Flag
        "G": 16,  # Last Active Year
        "H": 18,  # Papers (2022-2026)
        "I": 35,  # Recommended Action
        "J": 55,  # Profile URL
    }
    for col_let, w in widths.items():
        ws.column_dimensions[col_let].width = w

    wb.save(XLSX_PATH)
    print(f"[DONE] Beautiful Excel with native clickable links saved: {XLSX_PATH}")

if __name__ == "__main__":
    main()
