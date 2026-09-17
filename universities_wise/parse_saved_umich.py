from bs4 import BeautifulSoup
import re

with open('umich_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')
print("Title:", soup.title.string if soup.title else None)

# Inspect tags and classes
cards = soup.find_all(class_=lambda c: c and any(k in c.lower() for k in ['person', 'people', 'faculty', 'card', 'profile', 'entry', 'member']))
print("Cards count:", len(cards))

# Let's inspect some of these cards
for c in cards[:5]:
    print("Class:", c.get('class'))
    print("Text:", c.get_text(separator=' | ', strip=True)[:250])
    print("-" * 40)

# If no specific cards, find headers with names
if not cards:
    headings = soup.find_all(['h2', 'h3', 'h4'])
    print("Headings count:", len(headings))
    for h in headings[:10]:
        print("Heading:", h.get_text(strip=True))
