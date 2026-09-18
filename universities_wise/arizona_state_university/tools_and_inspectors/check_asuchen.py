import cloudscraper
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
r = scraper.get("https://search.asu.edu/profile/asuchen")
print("Status:", r.status_code)
for m in re.finditer(r'scholar|citation', r.text, re.IGNORECASE):
    start = max(0, m.start() - 100)
    end = min(len(r.text), m.end() + 100)
    print("MATCH:", r.text[start:end])
