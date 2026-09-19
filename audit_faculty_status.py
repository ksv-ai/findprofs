"""
audit_faculty_status.py
=======================
Audits every faculty member across the workbook to identify:
  1. Professor rank (Assistant Professor, Associate Professor, Full Professor)
  2. Potential Emeritus / Emerita / Retired
  3. Adjunct / Visiting / Lecturer / Research Scientist
  4. Inactivity (OpenAlex publication history since 2022)

Writes results progressively to 'faculty_status_audit.csv'.
"""

import sys
import io
import csv
import re
from pathlib import Path
import requests
import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed

# Force unbuffered UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True)

EXCEL_PATH = Path(r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx")
OUTPUT_REPORT = Path(r"d:\Others\findprofs\faculty_status_audit.csv")
OPENALEX_KEY = "NzjuLll4FIEV5HFS2mCK4g"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def analyze_profile_page(url):
    """Fetches profile URL and searches for faculty rank/title keywords."""
    if not url or not str(url).startswith("http"):
        return "NO_URL", "None"
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code != 200:
            return f"HTTP_{r.status_code}", "None"
        text = r.text.lower()

        # Check negative titles first
        if "emeritus" in text or "emerita" in text:
            return "FLAG_EMERITUS", "Emeritus"
        if "retired" in text or "retiree" in text:
            return "FLAG_RETIRED", "Retired"
        if "adjunct" in text and "assistant" not in text and "associate" not in text:
            return "FLAG_ADJUNCT", "Adjunct"
        if "lecturer" in text or "instructor" in text:
            return "FLAG_LECTURER", "Lecturer"

        # Check positive tenure-track ranks
        if "assistant professor" in text:
            return "ACTIVE_ASSISTANT_PROF", "Assistant Professor"
        if "associate professor" in text:
            return "ACTIVE_ASSOCIATE_PROF", "Associate Professor"
        if "professor" in text:
            return "ACTIVE_PROFESSOR", "Professor"

        return "UNCERTAIN_WEB", "No clear rank detected"
    except Exception as e:
        return "WEB_TIMEOUT", "Timeout"

def check_openalex_activity(oa_id):
    """Checks OpenAlex publication counts in recent years (2022-2026)."""
    if not oa_id or not str(oa_id).startswith("A"):
        return "NO_OA_ID", 0
    try:
        url = f"https://api.openalex.org/authors/{oa_id}"
        r = requests.get(url, headers={"Authorization": f"Bearer {OPENALEX_KEY}"}, timeout=5)
        if r.status_code != 200:
            return f"OA_{r.status_code}", 0
        d = r.json()
        counts_by_year = d.get("counts_by_year", [])
        recent_works = sum(y.get("works_count", 0) for y in counts_by_year if y.get("year", 0) >= 2022)
        last_pub_year = counts_by_year[0].get("year", 0) if counts_by_year else 0
        return f"LAST_{last_pub_year}", recent_works
    except Exception as e:
        return "OA_TIMEOUT", 0

def process_faculty_row(row_info):
    sn, name, uni, oa_id, profile_url = row_info
    web_flag, web_title = analyze_profile_page(profile_url)
    oa_status, recent_works = check_openalex_activity(oa_id)

    recommendation = "KEEP (Active Professor)"
    if "EMERITUS" in web_flag or "RETIRED" in web_flag:
        recommendation = "REMOVE (Emeritus / Retired)"
    elif "ADJUNCT" in web_flag or "LECTURER" in web_flag:
        recommendation = "REMOVE (Adjunct / Lecturer)"
    elif recent_works == 0 and "ACTIVE" not in web_flag:
        recommendation = "REVIEW (Inactive: 0 papers since 2022)"

    return [sn, name, uni, oa_id, web_title, web_flag, oa_status, recent_works, recommendation, profile_url]

def main():
    print(f"Loading workbook: {EXCEL_PATH}", flush=True)
    wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True)
    ws = wb["Master - All Live Verified"]

    tasks = []
    # Read rows: 1: S.N., 2: Name, 3: University, 6: OpenAlex ID, 9: Official Profile URL
    for r in ws.iter_rows(min_row=2, values_only=True):
        sn = r[0]
        name = r[1]
        uni = r[2]
        oa_id = str(r[5] or "").strip()
        profile_url = str(r[8] or "").strip()
        tasks.append((sn, name, uni, oa_id, profile_url))

    print(f"Total faculty to audit in Master: {len(tasks)}", flush=True)

    # Prepare CSV and write header immediately
    f_out = open(OUTPUT_REPORT, "w", newline="", encoding="utf-8", buffering=1)
    writer = csv.writer(f_out)
    writer.writerow([
        "S.N.", "Name", "University", "OpenAlex ID",
        "Detected Title", "Web Status Flag", "Last Active Year",
        "Papers (2022-2026)", "Recommended Action", "Profile URL"
    ])
    f_out.flush()

    completed = 0
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(process_faculty_row, t): t for t in tasks}
        for future in as_completed(futures):
            res = future.result()
            writer.writerow(res)
            f_out.flush()
            completed += 1
            if completed % 50 == 0 or completed == len(tasks):
                print(f"  Progress: [{completed}/{len(tasks)}] faculty audited ({completed/len(tasks)*100:.1f}%)", flush=True)

    f_out.close()
    print("\n[DONE] Faculty status audit complete! Check faculty_status_audit.csv", flush=True)

if __name__ == "__main__":
    main()
