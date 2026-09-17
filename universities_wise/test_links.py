import cloudscraper
from bs4 import BeautifulSoup

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
r = cs.get('https://aero.engin.umich.edu/')
print('Homepage status:', r.status_code)
soup = BeautifulSoup(r.text, 'lxml')
links = soup.find_all('a', href=True)
print('Total links:', len(links))
fac_links = set()
for a in links:
    href = a['href']
    text = a.get_text(strip=True).lower()
    if any(k in href.lower() or k in text for k in ['people', 'faculty', 'directory', 'staff']):
        fac_links.add((a.get_text(strip=True), href))

for text, href in sorted(fac_links):
    print(f"  {text} -> {href}")
