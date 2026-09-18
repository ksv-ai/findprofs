import cloudscraper
import pandas as pd
import json
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# 1. Fetch raw directory data to scan every single JSON field
url = "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered?dept_ids=1662&employee_types=Faculty,Faculty%20w/Admin%20Appointment&size=100"
r = scraper.get(url)
data = r.json().get("results", [])

id_map = {}

for item in data:
    name = item.get("display_name", {}).get("raw")
    text_blob = json.dumps(item)
    m = re.search(r'citations\?[^"\'\s<>]*user=([a-zA-Z0-9_-]{12})', text_blob)
    if not m:
        m = re.search(r'scholar\.google\.com/citations\?user=([a-zA-Z0-9_-]{12})', text_blob)
    if m:
        id_map[name] = m.group(1)

print(f"IDs found directly from JSON blob: {len(id_map)}")
for k, v in id_map.items():
    print(f"  {k} -> {v}")
