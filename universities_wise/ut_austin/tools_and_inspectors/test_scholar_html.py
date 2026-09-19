import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
name = "Marcus Herrmann"
query = f"{name} Arizona State University"
url = f"https://scholar.google.com/citations?view_op=search_authors&mauthors={query}"
r = scraper.get(url)
soup = BeautifulSoup(r.text, "lxml")
print("Page length:", len(r.text))
profiles = soup.find_all(class_=re.compile(r"gs_ai"))
print(f"gs_ai elements: {len(profiles)}")
for p in profiles:
    link = p.find("a", href=True)
    if link:
        print("Profile link:", link['href'], link.get_text(strip=True))

# Check for all /citations?user=
matches = re.findall(r'/citations\?user=[a-zA-Z0-9_-]+', r.text)
print("Regex matches:", set(matches))
