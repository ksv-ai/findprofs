import cloudscraper
import pandas as pd

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
df = pd.read_csv(r"d:\Others\findprofs\universities_wise\arizona_state_university\asu_aerospace_mechanical_faculty.csv")

print("Checking first 10 profile URLs:")
for idx, row in df.head(10).iterrows():
    name = row["Name"]
    url = row["Profile URL"]
    try:
        r = scraper.get(url, timeout=10)
        print(f"[{r.status_code}] {name} -> {url} (final: {r.url})")
    except Exception as e:
        print(f"[ERR] {name} -> {url}: {e}")
