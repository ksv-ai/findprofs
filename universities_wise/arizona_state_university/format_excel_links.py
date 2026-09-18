import pandas as pd

# Load CSV
csv_all = r"d:\Others\findprofs\universities_wise\arizona_state_university\asu_aerospace_mechanical_faculty.csv"
csv_matched = r"d:\Others\findprofs\universities_wise\arizona_state_university\asu_aerospace_mechanical_faculty_field_matched.csv"
excel_path = r"d:\Others\findprofs\universities_wise\arizona_state_university\asu_aerospace_mechanical_faculty.xlsx"

df = pd.read_csv(csv_all)

# Save Excel with native clickable HYPERLINK formulas
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='All Faculty', index=False)
    
    # Also write Field Matched sheet
    df_matched = df[df["Is Field Match"] == True].copy()
    df_matched.to_excel(writer, sheet_name='Field Matched', index=False)

    for sheetname in ['All Faculty', 'Field Matched']:
        ws = writer.sheets[sheetname]
        # Find column indices for Profile URL and Google Scholar URL
        header = [cell.value for cell in ws[1]]
        prof_col = header.index("Profile URL") + 1 if "Profile URL" in header else None
        scholar_col = header.index("Google Scholar URL") + 1 if "Google Scholar URL" in header else None
        email_col = header.index("Email") + 1 if "Email" in header else None

        for row in range(2, ws.max_row + 1):
            if prof_col:
                val = ws.cell(row=row, column=prof_col).value
                if val and str(val).startswith("http"):
                    cell = ws.cell(row=row, column=prof_col)
                    cell.hyperlink = str(val)
                    cell.style = "Hyperlink"
            if scholar_col:
                val = ws.cell(row=row, column=scholar_col).value
                if val and str(val).startswith("http"):
                    cell = ws.cell(row=row, column=scholar_col)
                    cell.hyperlink = str(val)
                    cell.style = "Hyperlink"
            if email_col:
                val = ws.cell(row=row, column=email_col).value
                if val and "@" in str(val):
                    cell = ws.cell(row=row, column=email_col)
                    cell.hyperlink = f"mailto:{val}"
                    cell.style = "Hyperlink"

print("Excel workbook created with active, clickable hyperlinks.")
