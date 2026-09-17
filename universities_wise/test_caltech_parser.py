import cloudscraper
from bs4 import BeautifulSoup
import re

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
r = cs.get('https://www.eas.caltech.edu/people/faculty')
soup = BeautifulSoup(r.text, 'lxml')

profile_links = [a for a in soup.find_all('a', href=True) if '/people/' in a['href'] and a['href'].count('/') == 2 and a.text.strip()]

faculty_entries = []
seen = set()
for a in profile_links:
    name = a.text.strip()
    href = a['href']
    if name in seen:
        continue
    if any(k in href.lower() for k in ['directory', 'leadership', 'staff', 'faculty', 'emeritus', 'lecturer', 'scholar', 'teaching', 'postdoc', 'resources']):
        continue
    seen.add(name)
    parent = a.find_parent('div')
    text = parent.get_text(separator=' | ', strip=True) if parent else ''
    full_url = f"https://www.eas.caltech.edu{href}" if href.startswith('/') else href
    faculty_entries.append((name, full_url, text))

print(f"Total Caltech faculty extracted: {len(faculty_entries)}")
for n, u, t in faculty_entries[:5]:
    print(f"  {n:<25} -> {u} | {t[:80]}")
