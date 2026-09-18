import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
uid = "HRx2lJQAAAAJ"
url = f"https://scholar.google.com/citations?user={uid}&hl=en"
r = scraper.get(url)

soup = BeautifulSoup(r.text, "lxml")
print("Title:", soup.title.get_text() if soup.title else "")
print("HTML length:", len(r.text))

# Search for "Cited by"
lines = [l for l in r.text.split("\n") if "cited" in l.lower()]
print(f"Lines containing cited: {len(lines)}")
for l in lines[:5]:
    print(" ", l[:150])

# Check table or stats div
table = soup.find("table", id="gsc_rsb_st")
if table:
    print("Found table gsc_rsb_st:")
    for tr in table.find_all("tr"):
        print([td.get_text(strip=True) for td in tr.find_all(["th", "td"])])
