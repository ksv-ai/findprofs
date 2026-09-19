import cloudscraper
import re
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
r = scraper.get('https://search.asu.edu/profile/mherrma1')
soup = BeautifulSoup(r.text, 'html.parser')

# Look for address / office
addr = soup.find('address', class_='person-address')
if addr:
    street = addr.find('span', class_='person-street')
    city = addr.find('span', class_='person-city')
    print('Office Street:', street.get_text(strip=True) if street else None)
    print('Office City:', city.get_text(strip=True) if city else None)

# Look for phone
tels = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('tel:')]
print('Tels:', tels)

phones = re.findall(r'\b\d{3}[-.]\d{3}[-.]\d{4}\b', r.text)
print('Phones in text:', phones)
