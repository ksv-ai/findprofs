import csv
import io
import json
import os
import re
import sys
import time
import requests
import openpyxl

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

API_KEY = "NzjuLll4FIEV5HFS2mCK4g"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "FindProfs/1.0 (mailto:ksv.ai.research@gmail.com)",
}

FLAGGED_CSV = r"d:\Others\findprofs\flagged_non_aero_faculty_audit.csv"
CORRECTED_CSV = r"d:\Others\findprofs\corrected_openalex_id_audit.csv"
EXCEL_PATH = r"d:\Others\findprofs\OpenalexID_R1_FACULTY_RESEARCH_AERO_MECH.xlsx"

AERO_FLUIDS_KEYWORDS = [
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
    r"\bheat transfer\b", r"\bthermal\b", r"\bflight\b", r"\bspacecraft\b", r"\brheology\b"
]
COMPILED_AERO = [re.compile(p, re.IGNORECASE) for p in AERO_FLUIDS_KEYWORDS]

EXCLUDE_KEYWORDS = [
    r"\bpatient\w*", r"\bclinical\b", r"\bcancer\b", r"\bcellular\b",
    r"\bbiomedical\b", r"\bcardiovascular\b", r"\bblood\b", r"\bhemodynamic\w*",
    r"\bbone\b", r"\btissue\b", r"\bin vivo\b", r"\bin vitro\b", r"\bsurgery\b",
    r"\bdrug delivery\b", r"\bbio[- ]\w+", r"\bnanocomposite\b", r"\bprosthetic\b"
]
COMPILED_EXCLUDE = [re.compile(p, re.IGNORECASE) for p in EXCLUDE_KEYWORDS]


def score_candidate(author_obj: dict, target_uni: str, focus_text: str) -> tuple:
    """Evaluates an author candidate based on affiliation match, aero relevance, and focus match."""
    insts = [i.get("display_name", "") for i in (author_obj.get("last_known_institutions") or [])]
    insts_text = " ".join(insts).lower()
    uni_words = [w.lower() for w in target_uni.split() if len(w) > 3 and w.lower() not in ["university", "college", "institute", "state"]]
    has_uni_match = any(w in insts_text for w in uni_words) if uni_words else False

    topics = [t.get("display_name", "") for t in (author_obj.get("topics") or [])[:5]]
    topics_text = " ".join(topics).lower()

    aero_score = sum(1 for p in COMPILED_AERO if p.search(topics_text))
    exclude_score = sum(1 for p in COMPILED_EXCLUDE if p.search(topics_text))

    focus_score = 0
    if focus_text:
        focus_words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{4,}\b", focus_text) if w.lower() not in ["engineering", "department", "research"]]
        focus_score = sum(1 for w in focus_words if w in topics_text)

    # Composite score
    total_score = (aero_score * 3) + (focus_score * 2) - (exclude_score * 4)
    if has_uni_match:
        total_score += 10

    return total_score, has_uni_match, aero_score, topics


def search_better_id(name: str, uni: str, current_id: str, focus_text: str):
    """Queries OpenAlex for candidate authors and finds if a genuine Aero/Fluids profile exists."""
    url = f"https://api.openalex.org/authors?search={requests.utils.quote(name)}&per_page=15"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code != 200:
            return None
        results = r.json().get("results", [])
    except Exception:
        return None

    scored_candidates = []
    for cand in results:
        cand_id = cand.get("id", "").split("/")[-1]
        score, uni_match, aero_score, topics = score_candidate(cand, uni, focus_text)
        scored_candidates.append({
            "cand_id": cand_id,
            "display_name": cand.get("display_name", ""),
            "score": score,
            "uni_match": uni_match,
            "aero_score": aero_score,
            "topics": topics,
            "works_count": cand.get("works_count", 0),
        })

    # Sort descending by score
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)

    if not scored_candidates:
        return None

    best = scored_candidates[0]

    # If best is different from current and has good aero/uni alignment
    if best["cand_id"] != current_id:
        if best["aero_score"] >= 1 and (best["uni_match"] or best["score"] >= 5):
            return {
                "status": "NAMESAKE_MISMATCH_CORRECTED",
                "old_id": current_id,
                "new_id": best["cand_id"],
                "new_topics": best["topics"][:3],
                "confidence": "HIGH" if best["uni_match"] else "MEDIUM"
            }

    # If even the best candidate has 0 aero score
    if best["aero_score"] == 0:
        return {
            "status": "LEGITIMATE_NON_AERO_FACULTY",
            "old_id": current_id,
            "new_id": current_id,
            "new_topics": best["topics"][:3],
            "confidence": "VERIFIED_NON_AERO"
        }

    return {
        "status": "CURRENT_ID_IS_CORRECT",
        "old_id": current_id,
        "new_id": current_id,
        "new_topics": best["topics"][:3],
        "confidence": "UNCHANGED"
    }


def main():
    print("Loading flagged faculty and Excel metadata...")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb["Master - All Live Verified"]
    excel_meta = {}
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(r, 2).value or "").strip()
        focus = str(ws.cell(r, 4).value or "").strip()
        cat = str(ws.cell(r, 5).value or "").strip()
        excel_meta[name.lower()] = {"focus": focus, "cat": cat, "row": r}

    with open(FLAGGED_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        flagged_rows = list(reader)

    print(f"Total flagged profiles to re-examine: {len(flagged_rows)}")

    audit_results = []
    corrected_count = 0
    non_aero_count = 0

    for i, row in enumerate(flagged_rows, 1):
        name = row["Faculty Name"]
        uni = row["University"]
        curr_id = row["OpenAlex ID"]
        meta = excel_meta.get(name.lower(), {})
        focus_text = meta.get("focus", "")

        res = search_better_id(name, uni, curr_id, focus_text)
        time.sleep(0.12)  # Polite API pace

        if res and res["status"] == "NAMESAKE_MISMATCH_CORRECTED":
            corrected_count += 1
            print(f"[{i:3d}/{len(flagged_rows)}] [CORRECTED MISMATCH] {name} ({uni}): {curr_id} -> {res['new_id']} | {res['new_topics']}")
            audit_results.append({
                "name": name,
                "uni": uni,
                "row_in_master": meta.get("row", ""),
                "verdict": "NAMESAKE_MISMATCH_FOUND_AND_CORRECTED",
                "old_openalex_id": curr_id,
                "correct_openalex_id": res["new_id"],
                "verified_topics": " | ".join(res["new_topics"]),
                "notes": f"Replaced with true Aero/Fluids profile ({res['confidence']})"
            })
        elif res and res["status"] == "LEGITIMATE_NON_AERO_FACULTY":
            non_aero_count += 1
            audit_results.append({
                "name": name,
                "uni": uni,
                "row_in_master": meta.get("row", ""),
                "verdict": "GENUINE_NON_AERO_FACULTY",
                "old_openalex_id": curr_id,
                "correct_openalex_id": curr_id,
                "verified_topics": " | ".join(res["new_topics"]),
                "notes": "Faculty is in ME department but does pure Biomedical/Robotics/Materials research"
            })
        else:
            audit_results.append({
                "name": name,
                "uni": uni,
                "row_in_master": meta.get("row", ""),
                "verdict": "BORDERLINE_OR_VERIFIED_CURRENT",
                "old_openalex_id": curr_id,
                "correct_openalex_id": curr_id,
                "verified_topics": " | ".join(res["new_topics"] if res else []),
                "notes": "Current ID is the best available"
            })

    print("=" * 80)
    print(f"RE-EXAMINATION COMPLETED")
    print(f"Total Profiles Re-examined:              {len(flagged_rows)}")
    print(f"Confirmed Namesake Mismatches Corrected: {corrected_count}")
    print(f"Genuine Non-Aero Faculty in ME:          {non_aero_count}")
    print("=" * 80)

    with open(CORRECTED_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["name", "uni", "row_in_master", "verdict", "old_openalex_id", "correct_openalex_id", "verified_topics", "notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(audit_results)

    print(f"Full audit report exported to: {CORRECTED_CSV}")


if __name__ == "__main__":
    main()
