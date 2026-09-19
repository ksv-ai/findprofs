import os
import json
import re
import urllib.parse
import requests

OPENALEX_API_KEY = "JyKkBSgwqlZae8wfXCatfk"

TIER1_TARGETS = [
    # UT Austin ASE
    {"name": "Noel Clemens", "search": "Noel T. Clemens", "dept": "ASE"},
    {"name": "Philip Varghese", "search": "Philip L. Varghese", "dept": "ASE"},
    {"name": "Laxminarayan Raja", "search": "Laxminarayan L. Raja", "dept": "ASE"},
    {"name": "Fabrizio Bisetti", "search": "Fabrizio Bisetti", "dept": "ASE"},
    {"name": "David Goldstein", "search": "David B. Goldstein", "dept": "ASE"},
    {"name": "Thomas Underwood", "search": "Thomas C. Underwood", "dept": "ASE"},
    {"name": "Jesse Chan", "search": "Jesse Chan", "dept": "ASE"},
    {"name": "Thomas Hughes", "search": "Thomas J.R. Hughes", "dept": "ASE"},
    {"name": "Karen Willcox", "search": "Karen E. Willcox", "dept": "ASE"},
    {"name": "Clint Dawson", "search": "Clint Dawson", "dept": "ASE"},
    
    # UT Austin ME
    {"name": "Robert Moser", "search": "Robert D. Moser", "dept": "ME"},
    {"name": "David Bogard", "search": "David G. Bogard", "dept": "ME"},
    {"name": "Vaibhav Bahadur", "search": "Vaibhav Bahadur", "dept": "ME"},
    {"name": "Ofodike Ezekoye", "search": "Ofodike A. Ezekoye", "dept": "ME"},
    {"name": "Omar Ghattas", "search": "Omar Ghattas", "dept": "ME"},
    {"name": "George Biros", "search": "George Biros", "dept": "ME"},
    {"name": "Spencer Bryngelson", "search": "Spencer H. Bryngelson", "dept": "ME"},
    
    # UT Austin Math
    {"name": "Todd Arbogast", "search": "Todd Arbogast", "dept": "Math"},
    {"name": "Bjorn Engquist", "search": "Bjorn Engquist", "dept": "Math"},
    {"name": "Irene Gamba", "search": "Irene M. Gamba", "dept": "Math"},
    {"name": "Per-Gunnar Martinsson", "search": "Per-Gunnar Martinsson", "dept": "Math"},
    {"name": "Rachel Ward", "search": "Rachel Ward", "dept": "Math"},
    {"name": "Yen-Hsi Tsai", "search": "Yen-Hsi Richard Tsai", "dept": "Math"},
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
                if data.get("recent_works"):
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
        if any(k in insts.lower() for k in ["austin", "texas at austin", "oden"]):
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
        "university": "University of Texas at Austin",
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
    for t in TIER1_TARGETS:
        process_target(t, cache_dir)
