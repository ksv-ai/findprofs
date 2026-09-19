import os
import json
import re
import urllib.parse
import requests

OPENALEX_API_KEY = "JyKkBSgwqlZae8wfXCatfk"

CU_BOULDER_TIER1_TARGETS = [
    # Ann and H.J. Smead Aerospace Engineering Sciences
    {"name": "Iain Boyd", "search": "Iain D. Boyd", "dept": "Aerospace Engineering Sciences"},
    {"name": "Kenneth Jansen", "search": "Kenneth E. Jansen", "dept": "Aerospace Engineering Sciences"},
    {"name": "John Evans", "search": "John A. Evans", "dept": "Aerospace Engineering Sciences"},
    {"name": "Alireza Doostan", "search": "Alireza Doostan", "dept": "Aerospace Engineering Sciences"},
    {"name": "John Farnsworth", "search": "John A. Farnsworth", "dept": "Aerospace Engineering Sciences"},
    {"name": "Kurt Maute", "search": "Kurt Maute", "dept": "Aerospace Engineering Sciences"},
    {"name": "Brian Argrow", "search": "Brian M. Argrow", "dept": "Aerospace Engineering Sciences"},
    {"name": "Hisham Ali", "search": "Hisham Ali", "dept": "Aerospace Engineering Sciences"},
    {"name": "Robyn Macdonald", "search": "Robyn Macdonald", "dept": "Aerospace Engineering Sciences"},
    {"name": "Timothy K. Minton", "search": "Timothy K. Minton", "dept": "Aerospace Engineering Sciences"},
    {"name": "Mahmoud Hussein", "search": "Mahmoud I. Hussein", "dept": "Aerospace Engineering Sciences"},
    {"name": "James Nabity", "search": "James Nabity", "dept": "Aerospace Engineering Sciences"},
    {"name": "Sanghamitra Neogi", "search": "Sanghamitra Neogi", "dept": "Aerospace Engineering Sciences"},

    # Paul M. Rady Mechanical Engineering
    {"name": "Peter Hamlington", "search": "Peter E. Hamlington", "dept": "Paul M. Rady Mechanical Engineering"},
    {"name": "Greg Rieker", "search": "Gregory B. Rieker", "dept": "Paul M. Rady Mechanical Engineering"},
    {"name": "Nicole Labbe", "search": "Nicole J. Labbe", "dept": "Paul M. Rady Mechanical Engineering"},
    {"name": "Hope Michelsen", "search": "Hope A. Michelsen", "dept": "Paul M. Rady Mechanical Engineering"},
    {"name": "Debanjan Mukherjee", "search": "Debanjan Mukherjee", "dept": "Paul M. Rady Mechanical Engineering"},
    {"name": "Nathalie M. Vriend", "search": "Nathalie M. Vriend", "dept": "Paul M. Rady Mechanical Engineering"},
    {"name": "Nicole Xu", "search": "Nicole W. Xu", "dept": "Paul M. Rady Mechanical Engineering"},
    {"name": "Robert MacCurdy", "search": "Robert MacCurdy", "dept": "Paul M. Rady Mechanical Engineering"},

    # Applied Mathematics
    {"name": "Gregory Beylkin", "search": "Gregory Beylkin", "dept": "Applied Mathematics"},
    {"name": "Adrianna Gillman", "search": "Adrianna Gillman", "dept": "Applied Mathematics"},
    {"name": "Mark Hoefer", "search": "Mark A. Hoefer", "dept": "Applied Mathematics"},
    {"name": "Mark J. Ablowitz", "search": "Mark J. Ablowitz", "dept": "Applied Mathematics"},
    {"name": "Ian Grooms", "search": "Ian Grooms", "dept": "Applied Mathematics"},
    {"name": "Stephen Becker", "search": "Stephen Becker", "dept": "Applied Mathematics"},
]

def reconstruct_abstract(inverted_index):
    if not inverted_index or not isinstance(inverted_index, dict):
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join([w for _, w in word_positions])

def clean_work_obj(w):
    title = w.get("title") or ""
    doi = w.get("doi") or ""
    year = w.get("publication_year") or 0
    cites = w.get("cited_by_count") or 0
    loc = w.get("primary_location") or {}
    source = loc.get("source") or {}
    venue = source.get("display_name") or ""
    inv_index = w.get("abstract_inverted_index")
    abstract = reconstruct_abstract(inv_index)
    
    return {
        "title": title,
        "doi": doi,
        "publication_year": year,
        "cited_by_count": cites,
        "venue": venue,
        "abstract": abstract
    }

def process_target(target, cache_dir):
    name = target["name"]
    search_q = target["search"]
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', name.strip().lower()).strip('_')
    cache_path = os.path.join(cache_dir, f"{slug}.json")
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f_ex:
                data = json.load(f_ex)
                if data.get("recent_works") and len(data["recent_works"]) >= 3:
                    print(f"Skipping already cached: {name} ({len(data['recent_works'])} works)")
                    return
        except Exception:
            pass
    
    print(f"\nFetching OpenAlex for: {name} (search: '{search_q}')...")
    url = f"https://api.openalex.org/authors?search={urllib.parse.quote(search_q)}&api_key={OPENALEX_API_KEY}"
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        print(f"Failed author search: {r.status_code}")
        return
    
    results = r.json().get("results", [])
    matched = None
    for a in results[:10]:
        insts = " ".join([i.get("display_name", "") for i in (a.get("last_known_institutions") or [])])
        if any(k in insts.lower() for k in ["colorado", "boulder"]):
            matched = a
            break
            
    if not matched and results:
        # Fallback to display name matching
        for a in results[:5]:
            if name.split()[-1].lower() in a.get("display_name", "").lower():
                matched = a
                break
        if not matched:
            matched = results[0]
            
    if not matched:
        print(f"No author found for {name}")
        return
        
    auth_id = matched.get("id")
    safe_disp = matched.get('display_name', '').encode('ascii', 'replace').decode('ascii')
    print(f"Found author: {safe_disp} ({auth_id})")
    
    # Extract topics
    topics = matched.get("topics", [])
    top_topics = [{"topic": t.get("display_name"), "count": t.get("count")} for t in topics[:5]]
    
    # 1. Fetch top cited works
    works_url = f"https://api.openalex.org/works?filter=author.id:{auth_id}&sort=cited_by_count:desc&per-page=5&api_key={OPENALEX_API_KEY}"
    r_top = requests.get(works_url, timeout=15)
    top_works = []
    if r_top.status_code == 200:
        for w in r_top.json().get("results", []):
            top_works.append(clean_work_obj(w))
            
    # 2. Fetch recent works (2023-2026)
    recent_url = f"https://api.openalex.org/works?filter=author.id:{auth_id},publication_year:2023-2026&sort=publication_year:desc,cited_by_count:desc&per-page=10&api_key={OPENALEX_API_KEY}"
    r_rec = requests.get(recent_url, timeout=15)
    recent_works = []
    if r_rec.status_code == 200:
        for w in r_rec.json().get("results", []):
            cw = clean_work_obj(w)
            recent_works.append(cw)
            
    cache_data = {
        "faculty_name": name,
        "full_name": matched.get("display_name"),
        "department": target["dept"],
        "university": "University of Colorado Boulder",
        "author_id": auth_id.split('/')[-1] if '/' in auth_id else auth_id,
        "works_count": matched.get("works_count"),
        "cited_by_count": matched.get("cited_by_count"),
        "h_index": matched.get("summary_stats", {}).get("h_index"),
        "top_topics": top_topics,
        "top_cited_works": top_works,
        "recent_works": recent_works
    }
    
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully cached {len(recent_works)} recent works (with reconstructed abstracts) to {cache_path}")

if __name__ == '__main__':
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openalex_cache")
    os.makedirs(cache_dir, exist_ok=True)
    print(f"Harvesting OpenAlex intelligence for {len(CU_BOULDER_TIER1_TARGETS)} CU Boulder faculty...")
    for t in CU_BOULDER_TIER1_TARGETS:
        process_target(t, cache_dir)
    print("\nAll OpenAlex extractions completed successfully!")
