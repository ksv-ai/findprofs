import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Let's inspect jkim520 profile text and websites
url = "https://search.asu.edu/profile/jkim520"
r = scraper.get(url)
print("jkim520 status:", r.status_code)
# Look for any external links
soup = BeautifulSoup(r.text, "lxml")
for a in soup.find_all("a", href=True):
    href = a['href']
    if any(k in href for k in ["scholar", "orcid", "github", "linkedin", "researchgate", "google"]):
        print("Link:", href, a.get_text(strip=True))

# Test ORCID lookup for scholar if orcid exists
for a in soup.find_all("a", href=re.compile(r"orcid\.org")):
    print("ORCID:", a['href'])
