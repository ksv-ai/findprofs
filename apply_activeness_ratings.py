"""
apply_activeness_ratings.py
===========================
1. Adds 'Activeness Rating' column:
     1 = Keep (Active Professor)
     2 = Review (Ambiguous / Inactive 0 papers)
     3 = Remove (Emeritus, Retired, Adjunct, Lecturer)
2. Updates both:
     - faculty_status_audit.csv
     - faculty_status_audit.xlsx (with full-row coloring: 1=Green, 2=Yellow, 3=Red)
3. Direct clickable hyperlinks preserved on Profile URL.
"""

import csv
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

CSV_PATH = Path(r"d:\Others\findprofs\faculty_status_audit.csv")
XLSX_PATH = Path(r"d:\Others\findprofs\faculty_status_audit.xlsx")

def get_rating(action_str):
    s = str(action_str).upper()
    if "KEEP" in s:
        return 1
    elif "REVIEW" in s:
        return 2
    elif "REMOVE" in s:
        return 3
    return 2 # Default to Review if unclassified

def main():
    print(f"Reading: {CSV_PATH}")
    with open(CSV_PATH, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader)
        raw_rows = list(reader)

    # Insert 'Activeness Rating' column right after 'Recommended Action' (or before URL)
    # Header: ['S.N.', 'Name', 'University', 'OpenAlex ID', 'Detected Title', 'Web Status Flag', 'Last Active Year', 'Papers (2022-2026)', 'Recommended Action', 'Profile URL']
    # New Header: insert 'Activeness Rating' as col 10, 'Profile URL' as col 11
    if "Activeness Rating" in header:
        rating_idx = header.index("Activeness Rating")
        new_header = header
    else:
        rating_idx = 9 # insert before Profile URL
        new_header = header[:9] + ["Activeness Rating"] + header[9:]

    processed_rows = []
    for r in raw_rows:
        action_val = r[8]
        rating = get_rating(action_val)
        
        # Clean URL if it has =HYPERLINK formula wrapper
        url_val = r[-1]
        raw_url = url_val
        if 'HYPERLINK("' in url_val:
            parts = url_val.split('"')
            if len(parts) >= 2:
                raw_url = parts[1]

        row_data = r[:9] + [rating] + [raw_url]
        processed_rows.append(row_data)

    # Sort strictly by S.N. ascending
    processed_rows.sort(key=lambda r: int(r[0]) if str(r[0]).strip().isdigit() else 999999)

    # 1. Save updated CSV with HYPERLINK formula
    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(new_header)
        for r in processed_rows:
            url = str(r[-1]).strip()
            url_formula = f'=HYPERLINK("{url}","{url}")' if url.startswith("http") else url
            writer.writerow(r[:-1] + [url_formula])

    print(f"[DONE] Saved updated CSV: {CSV_PATH}")

    # 2. Build beautifully colored Excel workbook (entire row colored by rating)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Faculty Status Audit"

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    link_font = Font(name="Calibri", size=10, color="0000FF", underline="single")
    regular_font = Font(name="Calibri", size=10)
    bold_font = Font(name="Calibri", size=10, bold=True)
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )

    # Rating row fills
    fill_rating_1 = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # Soft Green
    fill_rating_2 = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # Soft Yellow
    fill_rating_3 = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # Soft Red / Coral

    # Write headers
    for c_idx, h in enumerate(new_header, start=1):
        cell = ws.cell(1, c_idx, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Write data with entire row colored based on Activeness Rating
    for r_idx, r in enumerate(processed_rows, start=2):
        rating = r[9] # Activeness Rating
        if rating == 1:
            row_fill = fill_rating_1
        elif rating == 2:
            row_fill = fill_rating_2
        else:
            row_fill = fill_rating_3

        for c_idx, val in enumerate(r, start=1):
            cell = ws.cell(r_idx, c_idx)
            cell.font = regular_font
            cell.fill = row_fill
            cell.border = thin_border

            # Column 1 (S.N.)
            if c_idx == 1:
                cell.value = int(val) if str(val).isdigit() else val
                cell.alignment = center_align
            # Column 8 (Papers count)
            elif c_idx == 8:
                cell.value = int(val) if str(val).isdigit() else val
                cell.alignment = center_align
            # Column 10 (Activeness Rating: 1, 2, or 3)
            elif c_idx == 10:
                cell.value = int(val)
                cell.font = bold_font
                cell.alignment = center_align
            # Column 11 (Profile URL)
            elif c_idx == 11:
                url = str(val).strip()
                cell.value = url
                if url.startswith("http"):
                    cell.hyperlink = url
                    cell.font = link_font
                cell.alignment = left_align
            else:
                cell.value = val
                cell.alignment = center_align if c_idx in [4, 6, 7] else left_align

    # Freeze header row
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(new_header))}{len(processed_rows)+1}"

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
        "J": 18,  # Activeness Rating
        "K": 55,  # Profile URL
    }
    for col_let, w in widths.items():
        ws.column_dimensions[col_let].width = w

    wb.save(XLSX_PATH)
    print(f"[DONE] Saved full-row colored Excel audit file: {XLSX_PATH}")

if __name__ == "__main__":
    main()
