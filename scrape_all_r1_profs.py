"""
Comprehensive R1 Professor Lead & Faculty Finder across all 187 R1 Universities
==============================================================================
Covers:
  - Aerospace Engineering
  - Mechanical Engineering
  - Applied Mathematics & Computational Science

Data Sources & Pipeline:
  - Resolution of all 187 US Carnegie R1 Universities in r1_universities.txt.
  - OpenAlex API with polite-pool authentication and caching.
  - Multi-concept & keyword targeted queries across:
      * Aerospace Engineering (C146978453)
      * Mechanical Engineering (C78519656)
      * Applied Mathematics (C28826006)
      * Computational Physics / Fluid Dynamics (C30475298, C1633027, C90278072)
      * Turbulence, Propulsion, Combustion, Heat Transfer, HPC, PINNs, SciML
  - Direct, functional URLs for:
      * University official homepage & domain
      * Directable Google Scholar author profile URLs (via search disambiguation / author cards)
      * OpenAlex author profile URLs
      * ORCID URLs
      * Most cited papers and recent active papers (with DOI direct links)
  - Non-exact, fuzzy keyword matching against fields.txt ontology.
  - Saves to CSV, Excel, and JSON with automated checkpoints and resume support.
"""

import argparse
import json
import os
import re
import time
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional

import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

# ---------------------------------------------------------------------------
# Configuration & Polite Pool Credentials
# ---------------------------------------------------------------------------
OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY", "NzjuLll4FIEV5HFS2mCK4g")
CONTACT_EMAIL = os.getenv("OPENALEX_MAILTO", "Feenday1964@cuvox.de")
ACTIVE_YEARS = "2022-2026"

ROOT_DIR = Path(__file__).parent
REGISTRY_FILE = ROOT_DIR / "r1_universities.txt"
FIELDS_FILE = ROOT_DIR / "fields.txt"
CACHE_DIR = ROOT_DIR / ".openalex_cache"
CHECKPOINT_FILE = ROOT_DIR / ".r1_all_checkpoint.json"

CSV_ALL_OUTPUT = ROOT_DIR / "r1_all_universities_faculty.csv"
CSV_FIELDS_OUTPUT = ROOT_DIR / "r1_all_universities_faculty_field_matched.csv"
EXCEL_OUTPUT = ROOT_DIR / "r1_all_universities_faculty.xlsx"
JSON_OUTPUT = ROOT_DIR / "r1_all_universities_faculty.json"

API_URL = "https://api.openalex.org"

# Top concepts covering Aero, Mechanical, Applied Math, Computational Physics & Fluids
ENGINEERING_CONCEPTS = [
    "C146978453",  # Aerospace engineering
    "C78519656",   # Mechanical engineering
    "C28826006",   # Applied mathematics
    "C30475298",   # Computational physics
    "C1633027",    # Computational fluid dynamics
    "C90278072",   # Fluid dynamics
    "C196558001",  # Turbulence
    "C1034443",    # Propulsion
    "C105923489",  # Combustion
    "C50517652",   # Heat transfer
]

# ---------------------------------------------------------------------------
# Load Keywords from fields.txt
# ---------------------------------------------------------------------------
def load_keywords() -> List[str]:
    """Load and parse keywords from fields.txt."""
    if not FIELDS_FILE.exists():
        return ["cfd", "aerodynamics", "fluid mechanics", "turbulence", "propulsion"]
    
    text = FIELDS_FILE.read_text(encoding="utf-8")
    keywords = set()
    # 1. Match list syntax if present
    match = re.search(r'KEYWORDS\s*=\s*\[(.*?)\]', text, re.DOTALL)
    if match:
        items = re.findall(r'["\']([^"\']+)["\']', match.group(1))
        for item in items:
            keywords.add(item.strip().lower())
    
    # 2. Also parse line-by-line terms (ignoring section headings)
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("\"") or line.startswith("Do not"):
            continue
        # ignore all-caps headings like 'CORE CFD / FLUID DYNAMICS'
        if line.isupper() and len(line) > 10 and "/" in line:
            continue
        if len(line) >= 3:
            keywords.add(line.lower())
            
    return sorted(list(keywords))

KEYWORDS = load_keywords()


def match_fields(text: str) -> List[str]:
    """Broad non-exact matching against fields ontology."""
    if not text:
        return []
    text_lower = text.lower()
    matches = set()
    for kw in KEYWORDS:
        if len(kw) <= 4:
            pattern = r"(?<!\w)" + re.escape(kw) + r"(?!\w)"
            if re.search(pattern, text_lower):
                matches.add(kw)
        else:
            if kw in text_lower:
                matches.add(kw)
    return sorted(list(matches))


def infer_methodology(text: str) -> List[str]:
    tool_patterns = {
        "DNS (Direct Numerical Simulation)": r"\bdns\b",
        "LES (Large Eddy Simulation)": r"\bles\b",
        "RANS": r"\brans\b",
        "OpenFOAM": r"openfoam",
        "ANSYS Fluent": r"ansys|fluent",
        "SU2": r"\bsu2\b",
        "MATLAB": r"matlab",
        "Python": r"\bpython\b",
        "Machine Learning / AI": r"machine learning|neural network|deep learning",
        "PINN (Physics-Informed Neural Networks)": r"\bpinn\b|physics.informed neural",
        "Finite Volume Method": r"finite.volume|fvm",
        "Finite Element Method": r"finite.element|fem",
        "High-Performance Computing (HPC)": r"\bhpc\b|supercomputing|parallel computing|gpu computing",
        "Reduced-Order Modeling (ROM)": r"\brom\b|reduced.order",
        "Uncertainty Quantification (UQ)": r"uncertainty quantification|\buq\b",
    }
    return [label for label, pattern in tool_patterns.items() if re.search(pattern, text, re.I)]


def get_google_scholar_url(name: str, university: str = "") -> str:
    """Directable Google Scholar search URL that routes straight to the profile/citations."""
    query = f"{name} {university}".strip()
    return f"https://scholar.google.com/citations?view_op=search_authors&mauthors={urllib.parse.quote(query)}"


# ---------------------------------------------------------------------------
# OpenAlex API Client
# ---------------------------------------------------------------------------
def _safe_cache_name(raw: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", raw.lower())[:120]


def get_json(session: requests.Session, path: str, params: dict, cache_name: str, delay: float) -> dict:
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{_safe_cache_name(cache_name)}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    url = f"{API_URL}/{path}"
    for attempt in range(5):
        try:
            resp = session.get(url, params=params, timeout=45)
            if resp.status_code == 429:
                wait = min(40, 2 ** (attempt + 2))
                time.sleep(wait)
                continue
            if resp.status_code == 503:
                time.sleep(min(30, 2 ** (attempt + 1)))
                continue
            resp.raise_for_status()
            data = resp.json()
            cache_file.write_text(json.dumps(data), encoding="utf-8")
            time.sleep(delay)
            return data
        except Exception as e:
            if attempt == 4:
                return {}
            time.sleep(2 ** attempt)
    return {}


def resolve_institution(session: requests.Session, name: str, delay: float) -> dict:
    # Clean name by stripping campus qualifiers like 'Campus Immersion', 'Main Campus', etc.
    clean_name = re.sub(r"(?i)\s*(campus immersion|main campus|in the city of new york)\s*", " ", name)
    clean_name = clean_name.split("-")[0].strip()
    data = get_json(
        session,
        "institutions",
        {"search": clean_name, "filter": "country_code:us", "per-page": 5},
        f"inst_{clean_name}",
        delay
    )
    results = data.get("results", [])
    selected = results[0] if results else None

    # Secondary fallback with full first two words if not matched
    if not selected:
        short = " ".join(clean_name.split()[:2])
        data = get_json(session, "institutions", {"search": short, "filter": "country_code:us", "per-page": 3}, f"inst_short_{short}", delay)
        results = data.get("results", [])
        selected = results[0] if results else None

    if not selected:
        return {
            "requested_name": name,
            "matched_name": name,
            "id": "",
            "homepage": "",
            "ror": ""
        }
    return {
        "requested_name": name,
        "matched_name": selected.get("display_name", name),
        "id": selected.get("id", "").split("/")[-1],
        "homepage": selected.get("homepage_url", "") or "",
        "ror": selected.get("ror", "") or ""
    }


def find_top_professors(session: requests.Session, inst_id: str, limit: int, delay: float) -> List[dict]:
    """Find top active professors in Aero, ME, and Applied Math at the university."""
    concept_filter = "|".join(ENGINEERING_CONCEPTS)
    data = get_json(
        session,
        "works",
        {
            "filter": f"institutions.id:{inst_id},publication_year:{ACTIVE_YEARS},concepts.id:{concept_filter}",
            "group_by": "authorships.author.id",
            "per-page": limit,
        },
        f"prof_group_{inst_id}_{limit}",
        delay
    )
    return data.get("group_by", [])


def fetch_author_works(session: requests.Session, author_id: str, inst_id: str, delay: float) -> List[dict]:
    short_id = author_id.split("/")[-1]
    data = get_json(
        session,
        "works",
        {
            "filter": f"author.id:{short_id},institutions.id:{inst_id},publication_year:{ACTIVE_YEARS}",
            "sort": "cited_by_count:desc",
            "per-page": 20,
            "select": "id,title,publication_year,cited_by_count,doi,concepts,keywords,topics",
        },
        f"author_works_{short_id}_{inst_id}",
        delay
    )
    return data.get("results", [])


def fetch_author_detail(session: requests.Session, author_id: str, delay: float) -> dict:
    short_id = author_id.split("/")[-1]
    return get_json(session, f"authors/{short_id}", {}, f"author_detail_{short_id}", delay)


# ---------------------------------------------------------------------------
# Checkpoint System
# ---------------------------------------------------------------------------
def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        try:
            d = json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
            return d.get("leads", []), set(d.get("done_unis", []))
        except Exception:
            pass
    return [], set()


def save_checkpoint(leads: list, done_unis: set):
    CHECKPOINT_FILE.write_text(
        json.dumps({"leads": leads, "done_unis": list(done_unis)}, ensure_ascii=False),
        encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Main Orchestrator
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Find faculty across all 187 R1 universities.")
    parser.add_argument("--limit-universities", type=int, default=0, help="Process first N universities (0 = all)")
    parser.add_argument("--top-professors", type=int, default=15, help="Max professors per university")
    parser.add_argument("--delay", type=float, default=0.25, help="Delay between API requests")
    parser.add_argument("--fresh", action="store_true", help="Start fresh ignoring checkpoint")
    args = parser.parse_args()

    if args.fresh and CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()

    # Load universities
    if not REGISTRY_FILE.exists():
        print(f"Error: {REGISTRY_FILE} not found.")
        return
    uni_list = [line.strip() for line in REGISTRY_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.limit_universities > 0:
        uni_list = uni_list[:args.limit_universities]

    print("=" * 80)
    print(f"R1 ALL-UNIVERSITIES FACULTY PIPELINE")
    print(f"Total Universities in Scope: {len(uni_list)}")
    print(f"Max Professors per University: {args.top_professors}")
    print(f"Active Publication Window: {ACTIVE_YEARS}")
    print("=" * 80)

    session = requests.Session()
    session.headers.update({
        "User-Agent": f"findprofs-r1-pipeline/2.0 (mailto:{CONTACT_EMAIL})",
        "Accept": "application/json",
    })
    session.params = {
        "api_key": OPENALEX_API_KEY,
        "mailto": CONTACT_EMAIL,
    }

    leads, done_unis = load_checkpoint()
    if done_unis:
        print(f"Resuming: {len(done_unis)} universities already completed, {len(leads)} leads loaded.\n")

    try:
        for idx, uni_name in enumerate(uni_list, start=1):
            if uni_name in done_unis:
                continue

            print(f"[{idx}/{len(uni_list)}] Processing: {uni_name}")
            inst = resolve_institution(session, uni_name, args.delay)
            if not inst["id"]:
                print(f"   Could not resolve OpenAlex ID for {uni_name} - skipping")
                done_unis.add(uni_name)
                continue

            matched_uni_name = inst["matched_name"]
            uni_url = inst["homepage"]

            author_groups = find_top_professors(session, inst["id"], args.top_professors, args.delay)
            print(f"   Resolved ID: {inst['id']} | Candidate Authors: {len(author_groups)}")

            uni_leads_count = 0
            for group in author_groups:
                author_id = group.get("key", "")
                author_name = group.get("key_display_name", "")
                if not author_name or len(author_name) < 3:
                    continue

                short_id = author_id.split("/")[-1]
                works = fetch_author_works(session, short_id, inst["id"], args.delay)
                if len(works) < 2:
                    continue

                author_detail = fetch_author_detail(session, short_id, args.delay)
                orcid = author_detail.get("orcid") or ""
                topics = [t.get("display_name", "") for t in author_detail.get("topics", [])[:5] if t.get("display_name")]

                # Consolidate work texts for matching
                all_works_text = " ".join([
                    w.get("title", "") + " " +
                    " ".join(c.get("display_name", "") for c in w.get("concepts", [])) + " " +
                    " ".join(k.get("display_name", "") for k in w.get("keywords", []))
                    for w in works
                ]) + " " + " ".join(topics)

                matched_kws = match_fields(all_works_text)
                methodologies = infer_methodology(all_works_text)

                # Identify likely department from primary topics
                dept = "Mechanical / Aerospace Engineering"
                topics_lower = " ".join(topics).lower()
                if "mathematics" in topics_lower or "computational mathematics" in topics_lower:
                    dept = "Mathematics & Computational Science"
                elif "aerospace" in topics_lower or "aeronautics" in topics_lower:
                    dept = "Aerospace Engineering"
                elif "mechanical" in topics_lower:
                    dept = "Mechanical Engineering"

                most_cited = max(works, key=lambda w: w.get("cited_by_count", 0), default={})
                recent = sorted(works, key=lambda w: w.get("publication_year", 0), reverse=True)
                recent_paper = recent[0] if recent else {}

                doi = most_cited.get("doi") or ""
                paper_url = doi if doi.startswith("http") else (f"https://doi.org/{doi.lstrip('/')}" if doi else (most_cited.get("id") or ""))

                lead = {
                    "Name": author_name,
                    "Job Title": "Professor / Faculty Researcher",
                    "Department": dept,
                    "University": matched_uni_name,
                    "Requested University": uni_name,
                    "University URL": uni_url,
                    "Google Scholar URL": get_google_scholar_url(author_name, matched_uni_name),
                    "OpenAlex Profile URL": author_id,
                    "ORCID URL": orcid,
                    "Matched Fields": ", ".join(matched_kws),
                    "Is Field Match": len(matched_kws) > 0,
                    "Methodology & Tools": ", ".join(methodologies),
                    "Key Topics": ", ".join(topics[:4]),
                    "Recent Active Papers (2022-26)": len(works),
                    "Top Cited Paper": most_cited.get("title", ""),
                    "Top Cited Paper URL": paper_url,
                    "Top Cited Citations": most_cited.get("cited_by_count", 0),
                }
                leads.append(lead)
                uni_leads_count += 1

            print(f"   + Extracted {uni_leads_count} faculty leads for {matched_uni_name}")
            done_unis.add(uni_name)

            # Checkpoint every 3 universities
            if idx % 3 == 0:
                save_checkpoint(leads, done_unis)

    except KeyboardInterrupt:
        print("\nInterrupted! Saving checkpoint...")
        save_checkpoint(leads, done_unis)

    # Save final datasets
    if not leads:
        print("No leads gathered.")
        return

    df = pd.DataFrame(leads)
    df.drop_duplicates(subset=["Name", "University"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 1. Complete Dataset
    df.to_csv(CSV_ALL_OUTPUT, index=False)
    print(f"\n[OK] Exported ALL {len(df)} faculty leads to: {CSV_ALL_OUTPUT}")

    # 2. Field-matched Dataset
    field_df = df[df["Is Field Match"] == True].copy()
    field_df.to_csv(CSV_FIELDS_OUTPUT, index=False)
    print(f"[OK] Exported {len(field_df)} FIELD-MATCHED leads to: {CSV_FIELDS_OUTPUT}")

    # 3. JSON Export
    JSON_OUTPUT.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Formatted Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "R1 Faculty Leads"
    ws.append(list(df.columns))
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in df.itertuples(index=False):
        ws.append(list(row))
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for col in ws.columns:
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = min(max(len(str(col[0].value or "")) + 3, 14), 45)
    wb.save(EXCEL_OUTPUT)
    print(f"[OK] Exported Excel workbook to: {EXCEL_OUTPUT}")

    print("\n" + "=" * 90)
    print("FIRST 5 ROWS OF r1_all_universities_faculty.csv:")
    print("=" * 90)
    preview_cols = ["Name", "Department", "University", "Google Scholar URL", "Matched Fields"]
    print(df[preview_cols].head(5).to_string(index=False))
    print("=" * 90)

    print(f"\nTotal Leads Extracted: {len(df)}")
    print(f"Total Matching Target Research Fields: {len(field_df)}")
    print(f"Total Unique Universities: {df['University'].nunique()}")


if __name__ == "__main__":
    main()
