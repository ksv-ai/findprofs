import cloudscraper
from bs4 import BeautifulSoup

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
r = cs.get('https://aero.engin.umich.edu/people/')
print('People page status:', r.status_code)
soup = BeautifulSoup(r.text, 'lxml')
print('Title:', soup.title.string if soup.title else None)

# Find all cards, links, headings
links = soup.find_all('a', href=True)
print('Total links:', len(links))
for a in links[:30]:
    if a.get_text(strip=True):
        print('  ', a.get_text(strip=True), '->', a['href'])

# Find person elements
persons = soup.find_all(class_=lambda c: c and any(k in c.lower() for k in ['person', 'faculty', 'card', 'profile', 'member']))
print('Person classes count:', len(persons))
for p in persons[:5]:
    print('  Tag:', p.name, p.get('class'), p.get_text(separator=' | ', strip=True)[:150])
