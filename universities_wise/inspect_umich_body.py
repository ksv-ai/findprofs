import cloudscraper
from bs4 import BeautifulSoup
import re

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
cs.get('https://aero.engin.umich.edu/')
r = cs.get('https://aero.engin.umich.edu/people/fidkowski-krzysztof/')
soup = BeautifulSoup(r.text, 'lxml')

main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'entry-content|content'))
if main_content:
    print("Main content found:", main_content.name, main_content.get('class'))
    print(main_content.get_text(separator=' \n ', strip=True)[:1000])
else:
    print("No main container, body text:")
    print(soup.body.get_text(separator=' \n ', strip=True)[:1000])
