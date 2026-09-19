import cloudscraper
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Test the endpoints
endpoints = [
    "https://search.asu.edu/api/v1/webdir-profiles/department?dept_ids=1662&size=100",
    "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered?dept_ids=1662&size=100",
    "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff?dept_ids=1662&size=100",
    "https://search.asu.edu/api/v1/webdir-search/web?dept_ids=1662&size=100"
]

for ep in endpoints:
    try:
        r = scraper.get(ep, timeout=15)
        print(f"Endpoint: {ep}\nStatus: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict):
                print("Keys:", data.keys())
                for k in ["results", "data", "records", "total"]:
                    if k in data:
                        val = data[k]
                        print(f"  {k}: {type(val)} (len: {len(val) if isinstance(val, (list, dict)) else val})")
            elif isinstance(data, list):
                print(f"List with {len(data)} items")
            print("-" * 50)
    except Exception as e:
        print("Err:", e)
