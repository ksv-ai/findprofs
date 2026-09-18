import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Test pulling isearch profile page HTML
test_asurites = ["mherrma1", "ypeet", "kramesh2", "jkim520", "adscotti", "chattopa", "kgarg24", "leixinma"]
for asurite in test_asurites:
    url = f"https://search.asu.edu/profile/{asurite}"
    r = scraper.get(url)
    m = re.search(r'scholar\.google\.com/citations\?[^"\'\s<>]+user=([a-zA-Z0-9_-]{12})', r.text)
    if not m:
        m = re.search(r'user=([a-zA-Z0-9_-]{12})', r.text)
    print(f"{asurite} (status {r.status_code}) -> Scholar user: {m.group(1) if m else None}")
