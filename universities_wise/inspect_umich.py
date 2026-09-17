import cloudscraper
from bs4 import BeautifulSoup
import re

cs = cloudscraper.create_scraper(
    interpreter='native',
    delay=1,
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

r = cs.get('https://aero.engin.umich.edu/people/')
print('Status:', r.status_code)
if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'lxml')
    print('Title:', soup.title.string if soup.title else None)
    
    # Save a snippet or inspect classes
    # Look for faculty cards or people items
    cards = soup.find_all(['div', 'article', 'li'], class_=lambda c: c and any(k in c.lower() for k in ['person', 'people', 'faculty', 'card', 'profile', 'entry', 'member']))
    print('Cards count:', len(cards))
    
    # Check what classes exist
    unique_classes = set()
    for tag in soup.find_all(True):
        if tag.get('class'):
            for cls in tag.get('class'):
                if any(k in cls.lower() for k in ['person', 'people', 'faculty', 'card', 'profile', 'item', 'member']):
                    unique_classes.add(cls)
    print('Relevant classes found:', sorted(unique_classes))

    # Let's inspect some sample cards
    for card in cards[:5]:
        print('--- Card:', card.get('class'), '---')
        print(card.get_text(separator=' | ', strip=True)[:300])
