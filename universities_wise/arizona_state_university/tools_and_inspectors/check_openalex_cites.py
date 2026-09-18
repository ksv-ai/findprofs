import requests
import json
import time

# Let's test OpenAlex author search for Kangping Chen at ASU
url = "https://api.openalex.org/authors"
params = {
    "search": "Kangping Chen",
    "mailto": "Feenday1964@cuvox.de",
    "api_key": "NzjuLll4FIEV5HFS2mCK4g"
}
r = requests.get(url, params=params)
data = r.json()
print("OpenAlex authors found:", len(data.get("results", [])))
for a in data.get("results", [])[:3]:
    name = a.get("display_name")
    affils = [i.get("display_name") for i in a.get("last_known_institutions", [])]
    cited_by = a.get("cited_by_count")
    works_count = a.get("works_count")
    h_index = a.get("summary_stats", {}).get("h_index")
    i10_index = a.get("summary_stats", {}).get("i10_index")
    print(f"{name} | {affils} | cited_by_count: {cited_by} | works: {works_count} | h_index: {h_index} | i10: {i10_index}")
