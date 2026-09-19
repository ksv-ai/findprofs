"""
fetch_openalex_ids.py
=====================
Fetches OpenAlex Author IDs for every faculty member in:
  OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx

Strategy (in order of priority):
  1. Search OpenAlex by display_name + institution affiliation
  2. Name-only fallback: take top result if name is exact match

Column added: Column 3 -> "OpenAlex ID"  (e.g. A1234567890)

Features:
  - RESUME support: skips rows already filled with an OpenAlex ID
  - Unicode-safe console output (replaces unencodable chars with '?')
  - Checkpoint save every 50 rows
  - Errors / ambiguities written to openalex_id_issues.csv
"""

import sys
import io
import time
import csv
import re
import unicodedata
from pathlib import Path

import requests
import openpyxl
from openpyxl.styles import PatternFill, Font

# Force UTF-8 output on Windows console (avoids cp1252 UnicodeEncodeError)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# -- Config ------------------------------------------------------------------
XLSX_PATH   = Path(r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx")
LOG_CSV     = Path(r"d:\Others\findprofs\openalex_id_issues.csv")
BASE_URL    = "https://api.openalex.org/authors"
API_KEY     = "NzjuLll4FIEV5HFS2mCK4g"   # third key - fresh budget
SLEEP_OK    = 0.15   # seconds between requests
SLEEP_SLOW  = 5.0    # back-off on 429
SLEEP_ERR   = 3.0    # back-off on other errors
CHECKPOINT  = 25     # save every N rows
START_FROM_IDX = 1580 # user requested run only from 1580 to the end

# colour fills
FILL_FOUND     = PatternFill("solid", fgColor="C6EFCE")   # green
FILL_UNCERTAIN = PatternFill("solid", fgColor="FFEB9C")   # yellow
FILL_ERROR     = PatternFill("solid", fgColor="FFC7CE")   # red

# -- Helpers -----------------------------------------------------------------
def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except Exception:
        pass


def normalise(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip().lower()


def uni_words(name: str) -> set:
    stop = {"university", "of", "the", "at", "and", "state",
            "college", "institute", "technology", "tech",
            "&", "-", "system"}
    return {w for w in normalise(name).split() if w not in stop}


def affil_matches(candidate_affils: list, target_uni: str) -> bool:
    target_words = uni_words(target_uni)
    if not target_words:
        return False
    for affil in candidate_affils:
        affil_words = uni_words(affil)
        overlap = target_words & affil_words
        if len(overlap) >= max(1, len(target_words) // 2):
            return True
    return False


def get_json(url: str, params: dict):
    """GET with retry; handles 429 and network errors."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "FindProfs/1.0 (mailto:ksv.ai.research@gmail.com)",
    }
    for attempt in range(4):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=25)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:
                wait = SLEEP_SLOW * (attempt + 1)
                safe_print(f"\n      [429 rate-limit] attempt {attempt+1}, sleeping {wait}s ...", flush=True)
                time.sleep(wait)
            else:
                safe_print(f"\n      [HTTP {r.status_code}] {r.text[:200]}", flush=True)
                time.sleep(SLEEP_ERR)
        except requests.RequestException as exc:
            safe_print(f"\n      [Network error attempt {attempt+1}]: {exc}", flush=True)
            time.sleep(SLEEP_ERR)
    return None


def search_author(name: str, university: str):
    """
    Search OpenAlex for author by name, then validate by affiliation.
    Returns (openalex_id_or_None, status_string).
    """
    params = {"search": name, "per-page": "10"}
    data = get_json(BASE_URL, params)
    if data is None:
        return None, "API_ERROR"

    results = data.get("results", [])
    if not results:
        return None, "NOT_FOUND_BY_NAME"

    # Try to match by affiliation
    for author in results:
        affils = []
        lki = author.get("last_known_institutions") or []
        for inst in lki:
            if inst and inst.get("display_name"):
                affils.append(inst["display_name"])
        if affil_matches(affils, university):
            oa_id = author.get("id", "").replace("https://openalex.org/", "")
            return oa_id, "FOUND_NAME+AFFIL"

    # Fallback: take top result if name is an exact match
    top = results[0]
    top_name = top.get("display_name", "")
    if normalise(top_name) == normalise(name):
        oa_id = top.get("id", "").replace("https://openalex.org/", "")
        return oa_id, "FOUND_EXACT_NAME_NO_AFFIL_MATCH"

    return None, "CANDIDATES_FOUND_NO_AFFIL_MATCH"


# -- Main --------------------------------------------------------------------
def main():
    safe_print(f"Loading workbook: {XLSX_PATH}")
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active

    headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    safe_print("Existing headers:", headers)

    TARGET_COL = 3
    if len(headers) >= TARGET_COL and headers[TARGET_COL - 1] == "OpenAlex ID":
        safe_print("Column 'OpenAlex ID' already exists at col 3 - resuming from where left off.")
        openalex_col = TARGET_COL
    else:
        safe_print(f"Inserting new column 'OpenAlex ID' at position {TARGET_COL}...")
        ws.insert_cols(TARGET_COL)
        ws.cell(1, TARGET_COL).value = "OpenAlex ID"
        ws.cell(1, TARGET_COL).font = Font(bold=True)
        openalex_col = TARGET_COL

    total_rows = ws.max_row
    safe_print(f"Total data rows: {total_rows - 1}\n")

    issues = []
    found_count = 0
    not_found_count = 0
    skipped_count = 0
    error_count = 0

    for row_idx in range(2, total_rows + 1):
        faculty_num = row_idx - 1
        if faculty_num < START_FROM_IDX:
            continue

        name       = str(ws.cell(row_idx, 1).value or "").strip()
        university = str(ws.cell(row_idx, 2).value or "").strip()
        existing   = ws.cell(row_idx, openalex_col).value

        # ── RESUME: skip rows already processed with valid ID ──
        if existing and str(existing).startswith("A") and len(str(existing)) > 5:
            skipped_count += 1
            continue

        label = f"[{faculty_num:4d}/{total_rows-1}] {name[:45]:<45} | {university[:38]:<38}"

        if not name:
            ws.cell(row_idx, openalex_col).value = "EMPTY_NAME"
            ws.cell(row_idx, openalex_col).fill = FILL_ERROR
            issues.append([row_idx, name, university, "EMPTY_NAME", ""])
            safe_print(f"{label}  -->  EMPTY_NAME", flush=True)
            error_count += 1
            continue

        safe_print(f"{label}  -->  ", end="", flush=True)

        oa_id, status = search_author(name, university)

        if oa_id:
            ws.cell(row_idx, openalex_col).value = oa_id
            if "NO_AFFIL_MATCH" in status:
                ws.cell(row_idx, openalex_col).fill = FILL_UNCERTAIN
                issues.append([row_idx, name, university, status, oa_id])
            else:
                ws.cell(row_idx, openalex_col).fill = FILL_FOUND
            safe_print(f"{oa_id}  [{status}]", flush=True)
            found_count += 1
        else:
            ws.cell(row_idx, openalex_col).value = f"NOT_FOUND ({status})"
            ws.cell(row_idx, openalex_col).fill = FILL_ERROR
            issues.append([row_idx, name, university, status, ""])
            safe_print(f"NOT FOUND [{status}]", flush=True)
            not_found_count += 1

        time.sleep(SLEEP_OK)

        # Save checkpoint every CHECKPOINT rows
        processed = found_count + not_found_count + error_count
        if processed % CHECKPOINT == 0:
            wb.save(XLSX_PATH)
            safe_print(f"\n  -- Checkpoint saved ({processed} processed so far) --\n", flush=True)

    # Final save
    wb.save(XLSX_PATH)
    safe_print(f"\nWorkbook saved: {XLSX_PATH}")

    # Write issues CSV
    with open(LOG_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Row", "Faculty Name", "University", "Status", "OpenAlex ID"])
        writer.writerows(issues)
    safe_print(f"Issues log saved: {LOG_CSV}")

    safe_print("\n" + "="*65)
    safe_print(f"  SUMMARY")
    safe_print(f"  Total faculty : {total_rows - 1}")
    safe_print(f"  Skipped (already done) : {skipped_count}")
    safe_print(f"  Found         : {found_count}")
    safe_print(f"  Not found     : {not_found_count}")
    safe_print(f"  Errors        : {error_count}")
    safe_print("="*65)


if __name__ == "__main__":
    main()
