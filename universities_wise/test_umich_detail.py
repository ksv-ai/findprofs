import cloudscraper
from bs4 import BeautifulSoup
import re

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
cs.get('https://aero.engin.umich.edu/')

sample_urls = [
    'https://aero.engin.umich.edu/people/cesnik-carlos-e-s/',
    'https://aero.engin.umich.edu/people/fidkowski-krzysztof/'
]
for u in sample_urls:
    r = cs.get(u)
    print(f"UMich {u} -> {r.status_code}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        # Email
        email_el = soup.find('a', href=re.compile(r'mailto:'))
        email = email_el['href'].replace('mailto:', '').strip() if email_el else "N/A"
        # Research text
        text = soup.get_text(separator=' ', strip=True)
        print(f"   Email: {email}")
        print(f"   Snippet: {text[500:800]}")
