"""Build research-professor leads for the supplied US R1 university registry.

OpenAlex supplies publication and author facts.  Contact, lab, and Google
Scholar fields are intentionally left for manual verification from official pages.

Polite-pool access: the hardcoded API key and mailto User-Agent are sent on
every request so OpenAlex routes us through its higher-rate-limit tier.

Usage:
    python find_advisor.py                          # all universities in r1_universities.txt
    python find_advisor.py --limit-universities 5   # quick smoke-test
    python find_advisor.py --top-professors 30      # more professors per university
    python find_advisor.py --delay 0.2              # increase inter-request pause
    python find_advisor.py --fresh                  # ignore checkpoint and restart
"""

import argparse
import json
import os
import re
import time
from pathlib import Path

import requests
from openpyxl import Workbook
from openpyxl.styles import Font

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# OpenAlex polite-pool API key - gives higher rate limits.
# Override with environment variable OPENALEX_API_KEY if needed.
OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY", "NzjuLll4FIEV5HFS2mCK4g")

# Contact e-mail included in User-Agent so OpenAlex can reach you (polite pool).
CONTACT_EMAIL = os.getenv("OPENALEX_MAILTO", "Feenday1964@cuvox.de")

ACTIVE_YEARS = "2022-2026"

KEYWORDS = [
    "CFD", "computational fluid dynamics", "computational fluid mechanics",
    "computational aerodynamics", "aerodynamics", "fluid mechanics",
    "compressible flow", "high-speed flow", "hypersonics", "turbulence",
    "shock waves", "gas dynamics", "aerothermodynamics", "DNS", "LES", "turbulent flows",
    "RANS", "numerical methods", "boundary-layer transition",
    "fluid-structure interaction", "aeroelasticity", "propulsion",
    "scramjets", "combustion", "reactive flows", "rarefied gas dynamics",
    "high-temperature flow", "aeroacoustics", "atmospheric entry", "uas", "uav", "drones",
    "spacecraft aerodynamics", "scientific computing", "computational physics",
    "numerical PDEs", "multiphysics", "physics-informed ML", "PINN",
]

SEARCH_TERMS = (
    "aerodynamics OR aerospace OR \"fluid mechanics\" OR turbulence OR "
    "combustion OR propulsion OR hypersonics OR \"computational physics\""
)

OUTPUT_DIR       = Path(__file__).parent
DEFAULT_REGISTRY = OUTPUT_DIR / "r1_universities.txt"
JSON_OUTPUT      = OUTPUT_DIR / "r1_professor_leads.json"
EXCEL_OUTPUT     = OUTPUT_DIR / "r1_professor_leads.xlsx"
CACHE_DIR        = OUTPUT_DIR / ".openalex_cache"
CHECKPOINT_FILE  = OUTPUT_DIR / ".checkpoint.json"

API_URL = "https://api.openalex.org"
POLITE_DELAY_SECONDS = 1.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(value):
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _safe_cache_name(raw):
    return re.sub(r"[^a-z0-9_]", "_", raw.lower())[:120]


def get_json(session, path, params, cache_name, delay):
    """Fetch JSON from OpenAlex with caching, retry, and polite back-off."""
    cache_file = CACHE_DIR / f"{_safe_cache_name(cache_name)}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))

    url = f"{API_URL}/{path}"
    last_error = None

    for attempt in range(6):
        try:
            response = session.get(url, params=params, timeout=60)
        except requests.ConnectionError as exc:
            last_error = exc
            wait = 2 ** attempt
            print(f"    Connection error (attempt {attempt+1}); retrying in {wait}s ...")
            time.sleep(wait)
            continue

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            wait = float(retry_after) if retry_after else min(60, 2 ** (attempt + 2))
            print(f"    Rate-limited (429); waiting {wait:g}s before retry ...")
            time.sleep(wait)
            last_error = requests.HTTPError("429 Rate Limited", response=response)
            continue

        if response.status_code == 503:
            wait = min(60, 2 ** (attempt + 1))
            print(f"    Service unavailable (503); waiting {wait:g}s ...")
            time.sleep(wait)
            last_error = requests.HTTPError("503 Unavailable", response=response)
            continue

        response.raise_for_status()
        data = response.json()
        cache_file.write_text(json.dumps(data), encoding="utf-8")
        time.sleep(delay)
        return data

    raise requests.RequestException(f"All retries exhausted for {url}") from last_error


# ---------------------------------------------------------------------------
# Institution resolution
# ---------------------------------------------------------------------------

def resolve_institution(session, name, delay):
    data = get_json(
        session,
        "institutions",
        {"search": name, "filter": "country_code:us", "per-page": 10},
        f"institution_{normalize(name).replace(' ', '_')}",
        delay,
    )
    candidates = data.get("results", [])
    target = normalize(name)
    exact = [item for item in candidates if normalize(item.get("display_name", "")) == target]
    selected = exact[0] if exact else (candidates[0] if candidates else None)

    if not selected:
        return {
            "requested_university": name,
            "matched_university": "",
            "openalex_institution_id": "",
            "ror_id": "",
            "university_url": "",
            "resolution_status": "not_found",
        }

    return {
        "requested_university": name,
        "matched_university": selected.get("display_name", ""),
        "openalex_institution_id": selected.get("id", "").rsplit("/", 1)[-1],
        "ror_id": selected.get("ror", "") or "",
        "university_url": selected.get("homepage_url", "") or "",
        "resolution_status": "exact" if exact else "search_match_verify",
    }


# ---------------------------------------------------------------------------
# Author & works data
# ---------------------------------------------------------------------------

def fetch_author_detail(session, author_id, delay):
    """Fetch full author record for ORCID, topics, affiliations, etc."""
    short_id = author_id.rsplit("/", 1)[-1] if "/" in author_id else author_id
    try:
        return get_json(
            session,
            f"authors/{short_id}",
            {},
            f"author_detail_{short_id}",
            delay,
        )
    except requests.RequestException:
        return {}


def author_works(session, author_id, institution_id, delay):
    short_id = author_id.rsplit("/", 1)[-1] if "/" in author_id else author_id
    return get_json(
        session,
        "works",
        {
            "filter": (
                f"author.id:{short_id},"
                f"institutions.id:{institution_id},"
                f"publication_year:{ACTIVE_YEARS}"
            ),
            "sort": "cited_by_count:desc",
            "per-page": 50,
            "select": (
                "id,title,publication_year,publication_date,"
                "cited_by_count,doi,primary_location,concepts,keywords,topics"
            ),
        },
        f"works_{short_id}_{institution_id}",
        delay,
    ).get("results", [])


# ---------------------------------------------------------------------------
# Keyword / field matching
# ---------------------------------------------------------------------------

def work_text(work):
    concepts = " ".join(item.get("display_name", "") for item in work.get("concepts", []))
    keywords = " ".join(item.get("display_name", "") for item in work.get("keywords", []))
    topics   = " ".join(item.get("display_name", "") for item in work.get("topics", []))
    return " ".join([work.get("title", ""), concepts, keywords, topics]).lower()


def matched_fields(works):
    text = " ".join(work_text(w) for w in works)
    return sorted(kw for kw in KEYWORDS if kw.lower() in text)


def infer_methodology(works):
    """Infer methodology / tools from publication text."""
    tool_patterns = {
        "DNS (Direct Numerical Simulation)": r"\bdns\b",
        "LES (Large Eddy Simulation)": r"\bles\b",
        "RANS": r"\brans\b",
        "DES (Detached Eddy Simulation)": r"\bdes\b",
        "OpenFOAM": r"openfoam",
        "ANSYS Fluent": r"ansys|fluent",
        "SU2": r"\bsu2\b",
        "MATLAB": r"matlab",
        "Python": r"\bpython\b",
        "Machine Learning / AI": r"machine learning|neural network|deep learning",
        "PINN": r"\bpinn\b|physics.informed neural",
        "Finite Volume Method": r"finite.volume",
        "Finite Element Method": r"finite.element",
        "Lattice Boltzmann": r"lattice.boltzmann",
        "Adjoint Methods": r"\badjoint\b",
        "Uncertainty Quantification": r"uncertainty quantification",
    }
    text = " ".join(work_text(w) for w in works)
    return [label for label, pattern in tool_patterns.items() if re.search(pattern, text, re.I)]


# ---------------------------------------------------------------------------
# Lead creation
# ---------------------------------------------------------------------------

def _paper_url(work):
    doi = work.get("doi", "")
    if doi:
        return doi if doi.startswith("http") else f"https://doi.org/{doi.lstrip('/')}"
    return work.get("id", "")


def create_lead(institution, author_summary, author_detail, works):
    recent       = sorted(works, key=lambda w: (w.get("publication_year") or 0), reverse=True)
    most_cited   = max(works, key=lambda w: w.get("cited_by_count", 0), default={})
    recent_paper = recent[0] if recent else {}
    fields       = matched_fields(works)
    methods      = infer_methodology(works)

    author_openalex_url = author_summary.get("id", "")
    orcid_url = (
        author_detail.get("orcid", "")
        or author_summary.get("orcid", "")
        or ""
    )

    topics = [
        t.get("display_name", "")
        for t in author_detail.get("topics", [])[:6]
        if t.get("display_name")
    ]

    research_hook = (
        f"I was particularly interested in your recent work on {', '.join(fields[:3])}."
        if fields
        else "Please review the professor's recent OpenAlex publications before writing the hook."
    )

    source_urls = [u for u in [institution["university_url"], author_openalex_url, orcid_url] if u]

    return {
        # University
        "university":                  institution["matched_university"],
        "requested_university":        institution["requested_university"],
        "university_url":              institution["university_url"],
        "engineering_graduate_school": "",
        # Professor
        "professor_name":              author_summary.get("display_name", ""),
        "email":                       "",
        "professor_profile_url":       "",
        "lab_name":                    "",
        "lab_url":                     "",
        "lab_objectives":              "",
        # Online Profiles
        "google_scholar_url":          "",
        "openalex_profile_url":        author_openalex_url,
        "orcid_url":                   orcid_url,
        # Research
        "fields_of_expertise":         fields,
        "openalex_topics":             topics,
        "methodology_tools_approach":  methods,
        "research_hook":               research_hook,
        # Papers
        "most_cited_paper":            most_cited.get("title", ""),
        "most_cited_paper_url":        _paper_url(most_cited),
        "most_cited_paper_citations":  most_cited.get("cited_by_count", 0),
        "most_cited_paper_year":       most_cited.get("publication_year", ""),
        "recent_paper":                recent_paper.get("title", ""),
        "recent_paper_url":            _paper_url(recent_paper),
        "recent_paper_year":           recent_paper.get("publication_year", ""),
        "recent_papers_count_2022_26": len(works),
        # Meta
        "openalex_institution_id":     institution["openalex_institution_id"],
        "data_status":                 "publication_data_ready__manual_contact_enrichment_required",
        "source_urls":                 source_urls,
    }


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export_results(leads, institutions):
    JSON_OUTPUT.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

    wb = Workbook()

    # Sheet 1: Professor Leads
    ws1 = wb.active
    ws1.title = "Professor Leads"
    headers = list(leads[0]) if leads else ["data_status"]
    ws1.append(headers)
    for cell in ws1[1]:
        cell.font = Font(bold=True)
    for lead in leads:
        ws1.append([", ".join(v) if isinstance(v, list) else v for v in lead.values()])
    ws1.freeze_panes = "A2"
    ws1.auto_filter.ref = ws1.dimensions
    for col in ws1.columns:
        letter = col[0].column_letter
        ws1.column_dimensions[letter].width = min(max(len(str(col[0].value)) + 2, 16), 50)

    # Sheet 2: Universities
    ws2 = wb.create_sheet("Universities")
    inst_headers = list(institutions[0]) if institutions else ["resolution_status"]
    ws2.append(inst_headers)
    for cell in ws2[1]:
        cell.font = Font(bold=True)
    for inst in institutions:
        ws2.append(list(inst.values()))
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = ws2.dimensions

    wb.save(EXCEL_OUTPUT)


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        try:
            data = json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
            return data.get("leads", []), data.get("institutions", []), set(data.get("done_names", []))
        except Exception:
            pass
    return [], [], set()


def save_checkpoint(leads, institutions, done_names):
    CHECKPOINT_FILE.write_text(
        json.dumps({"leads": leads, "institutions": institutions, "done_names": list(done_names)}),
        encoding="utf-8",
    )


def clear_checkpoint():
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Scrape OpenAlex for professor leads across US R1 universities."
    )
    parser.add_argument("--university-file",    type=Path,  default=DEFAULT_REGISTRY)
    parser.add_argument("--limit-universities", type=int,   default=0,
                        help="Process only the first N universities (0 = all)")
    parser.add_argument("--top-professors",     type=int,   default=20,
                        help="Max professors to collect per university")
    parser.add_argument("--delay",              type=float, default=POLITE_DELAY_SECONDS,
                        help="Seconds to sleep between API calls (minimum 0.5)")
    parser.add_argument("--fresh",              action="store_true",
                        help="Ignore checkpoint and start from scratch")
    args = parser.parse_args()

    delay = max(args.delay, 0.5)
    CACHE_DIR.mkdir(exist_ok=True)

    names = [
        line.strip()
        for line in args.university_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if args.limit_universities:
        names = names[:args.limit_universities]

    # HTTP session with polite-pool credentials on every request
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            f"findprofs-r1-research-export/2.0 "
            f"(mailto:{CONTACT_EMAIL}; https://github.com/ksv-ai/findprofs)"
        ),
        "Accept": "application/json",
    })
    # api_key added to every request automatically via session params
    session.params = {
        "api_key": OPENALEX_API_KEY,
        "mailto": CONTACT_EMAIL,
    }

    print(f"OpenAlex API key : {OPENALEX_API_KEY[:6]}...{OPENALEX_API_KEY[-4:]}")
    print(f"Contact e-mail   : {CONTACT_EMAIL}")
    print(f"Universities     : {len(names)}")
    print(f"Inter-call delay : {delay}s")
    print()

    if args.fresh:
        clear_checkpoint()
    leads, institutions, done_names = load_checkpoint()
    if done_names:
        print(f"Resuming from checkpoint - {len(done_names)} universities already done.\n")

    for index, name in enumerate(names, start=1):
        if name in done_names:
            print(f"[{index}/{len(names)}] Skipping (cached) {name}")
            continue

        print(f"[{index}/{len(names)}] {name}")
        try:
            institution = resolve_institution(session, name, delay)
            institutions.append(institution)

            if not institution["openalex_institution_id"]:
                print(f"  Could not resolve institution - skipping")
                done_names.add(name)
                continue

            broad = get_json(
                session,
                "works",
                {
                    "filter": (
                        f"institutions.id:{institution['openalex_institution_id']},"
                        f"publication_year:{ACTIVE_YEARS}"
                    ),
                    "search": SEARCH_TERMS,
                    "group_by": "authorships.author.id",
                    "per-page": args.top_professors,
                },
                f"authors_{institution['openalex_institution_id']}",
                delay,
            )

            groups = broad.get("group_by", [])[:args.top_professors]
            print(f"  Found {len(groups)} candidate authors")

            for group in groups:
                author_id = group.get("key", "")
                author_summary = {
                    "id":           author_id,
                    "display_name": group.get("key_display_name", ""),
                }
                short_id = author_id.rsplit("/", 1)[-1] if "/" in author_id else author_id
                works = author_works(session, short_id, institution["openalex_institution_id"], delay)
                if len(works) < 2:
                    continue

                author_detail = fetch_author_detail(session, short_id, delay)
                lead = create_lead(institution, author_summary, author_detail, works)
                leads.append(lead)
                print(f"    + {lead['professor_name']} ({len(works)} papers)")

        except requests.RequestException as exc:
            print(f"  Request failed: {exc}")
        except (KeyError, ValueError) as exc:
            print(f"  Data issue: {exc}")

        done_names.add(name)

        if index % 5 == 0:
            save_checkpoint(leads, institutions, done_names)
            print(f"  [checkpoint saved - {len(leads)} leads so far]")

    leads.sort(key=lambda lead: (lead["university"], -lead["recent_papers_count_2022_26"]))
    export_results(leads, institutions)
    clear_checkpoint()

    print()
    print(f"Saved {len(leads)} professor leads across {len(institutions)} universities")
    print(f"JSON  -> {JSON_OUTPUT}")
    print(f"Excel -> {EXCEL_OUTPUT}")


if __name__ == "__main__":
    main()
