import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Test searching author on Google Scholar
name = "Marcus Herrmann"
query = f"{name} Arizona State University"
url = f"https://scholar.google.com/citations?view_op=search_authors&mauthors={query}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
r = scraper.get(url, headers=headers)
print("Status:", r.status_code)
print("Final URL:", r.url)
soup = BeautifulSoup(r.text, "lxml")
for a in soup.find_all("a", href=True):
    if "user=" in a['href']:
        print("Found author link:", a['href'], a.get_text(strip=True))
