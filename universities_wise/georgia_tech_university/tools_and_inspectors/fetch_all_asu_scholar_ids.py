import cloudscraper
import pandas as pd
import re
import time

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
csv_path = r"d:\Others\findprofs\universities_wise\arizona_state_university\asu_aerospace_mechanical_faculty.csv"
df = pd.read_csv(csv_path)

print(f"Total faculty to check: {len(df)}")
results = {}

for idx, row in df.iterrows():
    name = row["Name"]
    profile_url = row["Profile URL"]
    scholar_id = None
    
    if profile_url and "search.asu.edu/profile/" in profile_url:
        try:
            r = scraper.get(profile_url, timeout=12)
            if r.status_code == 200:
                # search for user= parameter with Scholar ID
                m = re.search(r'scholar\.google\.com/citations\?[^"\'\s<>]*user=([a-zA-Z0-9_-]{12})', r.text)
                if not m:
                    # sometimes relative or in href
                    m = re.search(r'citations\?user=([a-zA-Z0-9_-]{12})', r.text)
                if m:
                    scholar_id = m.group(1)
        except Exception as e:
            pass

    results[name] = scholar_id
    status_str = f"Found ID: {scholar_id}" if scholar_id else "No direct ID (uses search fallback)"
    print(f"[{idx+1}/{len(df)}] {name} -> {status_str}")
    time.sleep(0.3)

found_count = sum(1 for v in results.values() if v)
print(f"\nTotal faculty with direct Scholar ID found on profile: {found_count} / {len(df)}")
