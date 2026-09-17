import cloudscraper
from bs4 import BeautifulSoup
import re

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

# Test GaTech detail bio page
sample_urls = [
    'https://ae.gatech.edu/directory/person/krishan-k-ahuja',
    'https://ae.gatech.edu/directory/person/spencer-bryngelson'
]
for u in sample_urls:
    r = cs.get(u)
    print(f"GaTech {u} -> {r.status_code}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        # Title
        title_el = soup.find(class_=re.compile(r'field--name-field-title|title|field--name-field-position', re.I))
        title = title_el.get_text(strip=True) if title_el else "N/A"
        # Email
        email_el = soup.find('a', href=re.compile(r'mailto:'))
        email = email_el['href'].replace('mailto:', '').strip() if email_el else "N/A"
        # Research interests / bio
        res_el = soup.find(class_=re.compile(r'research|body|biography|interests', re.I))
        res_text = res_el.get_text(strip=True)[:150] if res_el else "N/A"
        print(f"   Title: {title}, Email: {email}")
        print(f"   Research snippet: {res_text}")
