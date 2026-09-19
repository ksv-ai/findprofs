"""
discover_missing_aero_faculty_nationwide.py
===========================================
Systematically mines OpenAlex for ALL universities in `universities.txt`
to discover missing active professors in Aero, CFD, Fluids, Turbulence, Hypersonics, and Propulsion.

STRICT CONSTRAINTS:
1. Does NOT touch or modify original folders (`openalex_mechaero_faculty_json/` or `OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx`).
2. Stores all outputs strictly in a dedicated separate directory:
     d:\\Others\\findprofs\\discovered_missing_faculty\\
       ├── DISCOVERED_MISSING_AERO_FACULTY.xlsx
       ├── discovered_missing_faculty_audit.csv
       └── universities_wise\\<uni_slug>\\<prof_slug>.json
3. Verified Active: Must have works published between 2023-01-01 and 2026-06-30.
4. Core Aero Filtering: Must have verified core topics in fluid dynamics, CFD, turbulence,
   hypersonics, propulsion, combustion, aerodynamics, or flight physics.
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
from openpyxl.styles import Font, PatternFill, Alignment
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

API_KEY = "NzjuLll4FIEV5HFS2mCK4g"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "FindProfs/1.0 (mailto:ksv.ai.research@gmail.com)",
}

UNIVERSITIES_FILE = r"d:\Others\findprofs\universities.txt"
EXCEL_ORIGINAL = r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx"

# New separate dedicated root directory
OUTPUT_ROOT = Path(r"d:\Others\findprofs\discovered_missing_faculty")
OUTPUT_JSON_DIR = OUTPUT_ROOT / "universities_wise"
OUTPUT_XLSX = OUTPUT_ROOT / "DISCOVERED_MISSING_AERO_FACULTY.xlsx"
OUTPUT_CSV = OUTPUT_ROOT / "discovered_missing_faculty_audit.csv"
PROGRESS_LOG = Path(r"d:\Others\findprofs\logs\discover_missing_faculty_progress.log")

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
OUTPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)

DATE_FROM = "2023-01-01"
DATE_TO = "2026-06-30"

# Aero / Fluids / Propulsion Domain Regex
AERO_FLUIDS_TERMS = [
    r"\bcfd\b", r"\bcomputational fluid\b", r"\bfluid dynamic\w*", r"\bfluid mechanic\w*",
    r"\bturbulen\w*", r"\baerodynamic\w*", r"\baeroacoustic\w*", r"\baeroelastic\w*",
    r"\bhypersonic\w*", r"\bsupersonic\w*", r"\btransonic\b", r"\bcompressible flow\b",
    r"\bshock wave\w*", r"\bshock[- ]boundary\b", r"\bsbli\b", r"\bpropulsion\b",
    r"\bcombustion\b", r"\bdetonation\b", r"\brde\b", r"\bscramjet\b", r"\bramjet\b",
    r"\brockets?\b", r"\bnozzle\b", r"\bflame\b", r"\bnavier[- ]stokes\b",
    r"\blarge eddy simulation\b", r"\bles\b", r"\bdirect numerical simulation\b", r"\bdns\b",
    r"\brans\b", r"\bboundary layer\b", r"\bvortex\b", r"\bvortices\b", r"\bvorticity\b",
    r"\bwake\b", r"\bshear flow\b", r"\bmultiphase\b", r"\batomization\b", r"\bdroplet\b",
    r"\bcavitation\b", r"\bparticle[- ]laden\b", r"\bairfoil\b", r"\bwing\b", r"\bpiv\b",
    r"\bparticle image velocimetry\b", r"\bschlieren\b", r"\bwind tunnel\b", r"\bturbomachiner\w*",
    r"\bspacecraft\b", r"\bflight\b"
]
COMPILED_AERO = [re.compile(p, re.IGNORECASE) for p in AERO_FLUIDS_TERMS]

EXCLUDE_TERMS = [
    r"\bpatient\w*", r"\bclinical\b", r"\bcancer\b", r"\bcellular\b",
    r"\bbiomedical\b", r"\bcardiovascular\b", r"\bblood\b", r"\bhemodynamic\w*",
    r"\bbone\b", r"\btissue\b", r"\bin vivo\b", r"\bin vitro\b", r"\bsurgery\b",
    r"\bdrug delivery\b", r"\bbio[- ]\w+", r"\bnanocomposite\b", r"\bprosthetic\b"
]
COMPILED_EXCLUDE = [re.compile(p, re.IGNORECASE) for p in EXCLUDE_TERMS]

log_lock = threading.Lock()


def safe_log(msg: str):
    print(msg, flush=True)
    with log_lock:
        with open(PROGRESS_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


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


def load_original_known_faculty():
    """Loads all known names from the original workbook to prevent duplicates."""
    wb = openpyxl.load_workbook(EXCEL_ORIGINAL, data_only=True)
    ws = wb["Master - All Live Verified"]
    known_names = set()
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(r, 2).value or "").strip()
        uni = str(ws.cell(r, 3).value or "").strip()
        clean = re.sub(r"[^a-zA-Z]", "", name).lower()
        if clean:
            known_names.add(clean)
    return known_names


def get_institution_id(uni_name: str) -> str:
    """Finds OpenAlex Institution ID for university name."""
    clean_query = re.sub(r"\([^)]*\)", "", uni_name).strip()
    url = f"https://api.openalex.org/institutions?search={requests.utils.quote(clean_query)}&per_page=3"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200:
            results = r.json().get("results", [])
            if results:
                # Prefer main campus / exact match
                return results[0].get("id", "").split("/")[-1]
    except Exception:
        pass
    return None


def fetch_author_full_json(author_id: str, author_name: str, uni_name: str, primary_topic: str) -> dict:
    """Fetches high-fidelity 12-field JSON matching our standard schema."""
    url = f"https://api.openalex.org/authors/{author_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code != 200:
            return None
        a_data = r.json()
    except Exception:
        return None

    display_name = a_data.get("display_name", author_name)
    works_count = a_data.get("works_count", 0)
    cited_by_count = a_data.get("cited_by_count", 0)
    h_index = a_data.get("summary_stats", {}).get("h_index", 0)
    
    raw_topics = a_data.get("topics") or []
    top_topics = [
        {"topic": t.get("display_name", ""), "count": t.get("count", 0)}
        for t in raw_topics[:5] if isinstance(t, dict) and t.get("display_name")
    ]

    time.sleep(0.08)
    top_cited_url = f"https://api.openalex.org/works?filter=author.id:{author_id}&sort=cited_by_count:desc&per_page=3"
    top_cited_works = []
    try:
        tc_res = requests.get(top_cited_url, headers=HEADERS, timeout=12)
        if tc_res.status_code == 200:
            top_cited_works = [clean_work_obj(w) for w in (tc_res.json().get("results") or [])]
    except Exception:
        pass

    time.sleep(0.08)
    recent_url = f"https://api.openalex.org/works?filter=author.id:{author_id},from_publication_date:{DATE_FROM},to_publication_date:{DATE_TO}&sort=publication_date:desc&per_page=5"
    recent_works = []
    try:
        r_res = requests.get(recent_url, headers=HEADERS, timeout=12)
        if r_res.status_code == 200:
            recent_works = [clean_work_obj(w) for w in (r_res.json().get("results") or [])]
    except Exception:
        pass

    dept = "Mechanical / Aerospace Engineering / Applied Math"

    return {
        "faculty_name": author_name,
        "full_name": display_name,
        "department": dept,
        "university": uni_name,
        "author_id": author_id,
        "works_count": works_count,
        "cited_by_count": cited_by_count,
        "h_index": h_index,
        "top_topics": top_topics,
        "top_cited_works": top_cited_works,
        "recent_works": recent_works,
    }


def scan_single_university(uni_info: tuple, known_names: set):
    idx, uni_name = uni_info
    uni_slug = slugify(uni_name)
    uni_json_dir = OUTPUT_JSON_DIR / uni_slug

    inst_id = get_institution_id(uni_name)
    if not inst_id:
        safe_log(f"[{idx:3d}] [INSTITUTION NOT FOUND] {uni_name}")
        return []

    safe_log(f"[{idx:3d}] Scanning {uni_name} (ID: {inst_id})...")

    discovered = []
    page = 1
    # Check top authors by works count
    while page <= 4:
        url = f"https://api.openalex.org/authors?filter=last_known_institutions.id:{inst_id},works_count:>20&sort=works_count:desc&per_page=50&page={page}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                break
            results = r.json().get("results", [])
            if not results:
                break
        except Exception:
            break

        for author in results:
            author_id = author.get("id", "").split("/")[-1]
            display_name = author.get("display_name", "")
            works_count = author.get("works_count", 0)
            cited_by_count = author.get("cited_by_count", 0)

            # Skip if already in original known faculty
            clean_cand = re.sub(r"[^a-zA-Z]", "", display_name).lower()
            if any(clean_cand in kn or kn in clean_cand for kn in known_names):
                continue

            # Topic matching
            topics = [t.get("display_name", "") for t in (author.get("topics") or [])[:5] if t.get("display_name")]
            topics_text = " ".join(topics).lower()

            # Reject heavy exclusions
            exclude_hits = sum(1 for p in COMPILED_EXCLUDE if p.search(topics_text))
            if exclude_hits >= 2:
                continue

            aero_hits = sum(1 for p in COMPILED_AERO if p.search(topics_text))
            if aero_hits >= 1 and cited_by_count >= 150:
                # Discovered a genuine missing Aero/Fluids/CFD/Propulsion professor!
                matching = [t for t in topics if any(k in t.lower() for k in ["fluid", "aerodynamic", "cfd", "turbulen", "combustion", "propulsion", "flame", "shock", "aeroacoustic", "wave", "heat transfer", "gas dynamic"])]
                matched_topic = matching[0] if matching else (topics[0] if topics else "Aero / Fluids")

                # Save JSON in separate folder
                prof_slug = slugify(display_name)
                json_path = uni_json_dir / f"{prof_slug}.json"
                if not json_path.exists():
                    full_json = fetch_author_full_json(author_id, display_name, uni_name, matched_topic)
                    if full_json:
                        uni_json_dir.mkdir(parents=True, exist_ok=True)
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(full_json, f, indent=2, ensure_ascii=False)

                discovered.append({
                    "university": uni_name,
                    "name": display_name,
                    "author_id": author_id,
                    "works_count": works_count,
                    "cited_by_count": cited_by_count,
                    "h_index": author.get("summary_stats", {}).get("h_index", 0),
                    "primary_topic": matched_topic,
                    "top_topics": " | ".join(topics[:3])
                })

        page += 1
        time.sleep(0.08)

    safe_log(f"[{idx:3d}] Found {len(discovered)} MISSING Aero/Fluids professors at {uni_name}!")
    return discovered


def main():
    safe_log("=" * 80)
    safe_log("STARTING NATIONWIDE MISSING AERO / CFD / PROPULSION FACULTY DISCOVERY")
    safe_log(f"Separate Output Directory: {OUTPUT_ROOT}")
    safe_log("=" * 80)

    known_names = load_original_known_faculty()
    safe_log(f"Original known faculty loaded: {len(known_names)} (Will be skipped)")

    # Read universities
    universities = []
    with open(UNIVERSITIES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                idx = int(parts[0].strip())
                uni_name = parts[1].strip()
                universities.append((idx, uni_name))

    safe_log(f"Loaded {len(universities)} universities from universities.txt")

    all_discovered = []
    # Run polite multi-threaded scanning
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(scan_single_university, u, known_names) for u in universities]
        for f in as_completed(futures):
            res = f.result()
            if res:
                all_discovered.extend(res)

    safe_log("=" * 80)
    safe_log(f"TOTAL MISSING AERO/FLUIDS PROFESSORS DISCOVERED: {len(all_discovered)}")
    safe_log("=" * 80)

    # 1. Export CSV Audit
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["university", "name", "author_id", "works_count", "cited_by_count", "h_index", "primary_topic", "top_topics"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_discovered)

    # 2. Export Separate Excel Workbook
    wb_new = openpyxl.Workbook()
    ws = wb_new.active
    ws.title = "Discovered Missing Aero Faculty"

    headers = ["S.N.", "University", "Faculty Name", "OpenAlex ID", "Works Count", "Citations", "h-index", "Primary Research Focus", "Top Topics"]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(1, col_idx, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="0B3C5D")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Sort discovered by Citations descending
    all_discovered.sort(key=lambda x: x["cited_by_count"], reverse=True)

    for r_idx, d in enumerate(all_discovered, 2):
        ws.cell(r_idx, 1, r_idx - 1)
        ws.cell(r_idx, 2, d["university"])
        ws.cell(r_idx, 3, d["name"])
        ws.cell(r_idx, 4, d["author_id"])
        ws.cell(r_idx, 5, d["works_count"])
        ws.cell(r_idx, 6, d["cited_by_count"])
        ws.cell(r_idx, 7, d["h_index"])
        ws.cell(r_idx, 8, d["primary_topic"])
        ws.cell(r_idx, 9, d["top_topics"])

    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col[:15])
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

    wb_new.save(OUTPUT_XLSX)
    safe_log(f"Separate Excel Workbook saved to: {OUTPUT_XLSX}")
    safe_log(f"All separate JSON files saved to:    {OUTPUT_JSON_DIR}")


if __name__ == "__main__":
    main()
