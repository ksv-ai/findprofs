import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
url = "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/"
resp = scraper.get(url, timeout=30)
soup = BeautifulSoup(resp.text, "lxml")

# Look at scripts
scripts = soup.find_all("script")
print(f"Total script tags: {len(scripts)}")
for s in scripts:
    src = s.get("src", "")
    if src:
        if any(x in src.lower() for x in ["directory", "people", "faculty", "asu", "api", "wp-json"]):
            print("Script src:", src)
    else:
        txt = s.string or ""
        if any(x in txt.lower() for x in ["pfpeople", "faculty", "directory", "semte", "api", "ajax"]):
            print("Inline script snippet:", txt[:300].strip(), "\n---")

# Look at div pfpeople-web-directory
target_div = soup.find(class_=re.compile(r"pfpeople|directory"))
if target_div:
    print("target_div attrs:", target_div.attrs)
    print("target_div html snippet:", str(target_div)[:500])
