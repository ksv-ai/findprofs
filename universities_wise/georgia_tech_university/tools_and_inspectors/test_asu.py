import cloudscraper
from bs4 import BeautifulSoup
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
url = "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

resp = scraper.get(url, headers=headers, timeout=30)
print(f"Status: {resp.status_code}")
print(f"Length: {len(resp.text)}")

soup = BeautifulSoup(resp.text, "lxml")
print("Title:", soup.title.get_text() if soup.title else "No title")

# Look for faculty cards or profile links
links = soup.find_all("a", href=True)
fac_links = [a for a in links if "faculty.engineering.asu.edu" in a['href'] or "/faculty/" in a['href']]
print(f"Total links: {len(links)}, matching fac_links: {len(fac_links)}")
for a in fac_links[:10]:
    print(a['href'], "-->", a.get_text(strip=True))

# Sample HTML structures
cards = soup.find_all(class_=lambda c: c and any(x in c.lower() for x in ['faculty', 'profile', 'person', 'directory', 'card', 'member']))
print(f"Possible cards/items count: {len(cards)}")
for c in cards[:5]:
    print(c.get('class'), c.get_text(strip=True)[:100])
