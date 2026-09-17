import cloudscraper
from bs4 import BeautifulSoup
import re

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
r = cs.get('https://ae.gatech.edu/directory/person/spencer-bryngelson')
soup = BeautifulSoup(r.text, 'lxml')

print("All field classes:")
for tag in soup.find_all(class_=re.compile(r'field')):
    cls = tag.get('class')
    print(" ", cls, "->", tag.get_text(strip=True)[:100])
