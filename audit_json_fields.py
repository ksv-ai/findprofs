import glob
import json
import os
import re
import csv

base = r"d:\Others\findprofs\openalex_mechaero_faculty_json\universities_wise"
files = glob.glob(os.path.join(base, "*", "*.json"))
print(f"Total JSON files present for audit: {len(files)}")

AERO_FLUIDS_TERMS = [
    r"\bcfd\b", r"\bfluid\b", r"\bfluids\b", r"\baero\w*", r"\bturbulen\w*",
    r"\bhypersonic\w*", r"\bsupersonic\w*", r"\btransonic\b", r"\bcompressible\b",
    r"\bpropulsion\b", r"\bcombustion\b", r"\bdetonation\b", r"\brde\b", r"\bscramjet\b",
    r"\bramjet\b", r"\brockets?\b", r"\bnozzle\b", r"\bflame\b", r"\bnavier[- ]stokes\b",
    r"\bles\b", r"\bdns\b", r"\brans\b", r"\bboundary layer\b", r"\bvortex\b", r"\bvortices\b",
    r"\bvorticity\b", r"\bwake\b", r"\bmultiphase\b", r"\batomization\b", r"\bdroplet\b",
    r"\bcavitation\b", r"\bairfoil\b", r"\bwing\b", r"\bpiv\b", r"\bschlieren\b",
    r"\bwind tunnel\b", r"\bheat transfer\b", r"\bthermal\b", r"\bflight\b", r"\baircraft\b"
]
COMPILED_AERO = [re.compile(p, re.IGNORECASE) for p in AERO_FLUIDS_TERMS]

SUSPICIOUS_TERMS = [
    r"\bclinical\b", r"\bcancer\b", r"\bpatient\b", r"\bcellular\b", r"\bbiomedical\b",
    r"\bcardiovascular\b", r"\bblood\b", r"\bsurgery\b", r"\bdrug delivery\b",
    r"\borthop\w*", r"\bbone\b", r"\btissue engineering\b", r"\bneuro\w*"
]
COMPILED_SUSP = [re.compile(p, re.IGNORECASE) for p in SUSPICIOUS_TERMS]

flagged = []

for fp in files:
    try:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        continue

    name = data.get("faculty_name", "")
    uni = data.get("university", "")
    author_id = data.get("author_id", "")
    dept = data.get("department", "")

    topics = [t.get("topic", "") for t in data.get("top_topics", [])]
    top_titles = [w.get("title", "") for w in data.get("top_cited_works", [])]
    recent_titles = [w.get("title", "") for w in data.get("recent_works", [])]

    combined_text = " ".join(topics + top_titles + recent_titles)

    aero_matches = [p.pattern for p in COMPILED_AERO if p.search(combined_text)]
    susp_matches = [p.pattern for p in COMPILED_SUSP if p.search(combined_text)]

    if len(aero_matches) == 0:
        flagged.append({
            "name": name,
            "uni": uni,
            "dept": dept,
            "author_id": author_id,
            "reason": "ZERO_AERO_OR_FLUIDS_MATCH",
            "top_topics": topics[:3],
            "sample_paper": top_titles[0] if top_titles else "None"
        })
    elif len(susp_matches) >= 3 and len(aero_matches) <= 1:
        flagged.append({
            "name": name,
            "uni": uni,
            "dept": dept,
            "author_id": author_id,
            "reason": "BIOMEDICAL_OR_CLINICAL_DOMINATED",
            "top_topics": topics[:3],
            "sample_paper": top_titles[0] if top_titles else "None"
        })

print(f"Total flagged non-aero/suspicious faculty: {len(flagged)}")
out_csv = r"d:\Others\findprofs\flagged_non_aero_faculty_audit.csv"
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Faculty Name", "University", "Department", "OpenAlex ID", "Reason", "Top Topics", "Sample Landmark Paper"])
    for item in flagged:
        writer.writerow([
            item["name"], item["uni"], item["dept"], item["author_id"],
            item["reason"], " | ".join(item["top_topics"]), item["sample_paper"]
        ])
print(f"Audit report written to: {out_csv}")

for i, item in enumerate(flagged[:15], 1):
    print(f"{i:2d}. {item['name']} ({item['uni']}) | ID: {item['author_id']}")
    print(f"    Reason: {item['reason']}")
    print(f"    Topics: {item['top_topics']}")
    print(f"    Paper:  {item['sample_paper'][:75]}")
