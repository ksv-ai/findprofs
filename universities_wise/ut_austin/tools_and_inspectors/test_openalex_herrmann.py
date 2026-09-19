import requests
import json

# OpenAlex author search
r = requests.get("https://api.openalex.org/authors?search=Marcus%20Herrmann")
data = r.json()
print("Total found:", len(data.get("results", [])))
for a in data.get("results", [])[:5]:
    insts = [aff.get("institution", {}).get("display_name") for aff in a.get("affiliations", []) if aff.get("institution")]
    last_inst = a.get("last_known_institutions", [])
    last_names = [i.get("display_name") for i in last_inst]
    print(f"- {a.get('display_name')} | Affils: {last_names} | ids: {a.get('ids')}")
