import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
profiles = ['adscotti', 'mherrma1', 'kchen', 'ypeet', 'kramesh1', 'achattop']

for asurite in profiles:
    r = scraper.get(f'https://search.asu.edu/profile/{asurite}')
    soup = BeautifulSoup(r.text, 'html.parser')
    addr = soup.find('address', class_='person-address')
    street = addr.find('span', class_='person-street').get_text(strip=True) if addr and addr.find('span', class_='person-street') else ''
    city = addr.find('span', class_='person-city').get_text(strip=True) if addr and addr.find('span', class_='person-city') else ''
    mail_code_el = soup.find('div', class_='mail-code')
    mail_code = mail_code_el.get_text(strip=True) if mail_code_el else ''
    campus_el = soup.find('div', class_='campus')
    campus = campus_el.get_text(strip=True) if campus_el else ''
    
    # Check phone
    phone_el = soup.find('a', href=lambda x: x and x.startswith('tel:'))
    phone = phone_el.get_text(strip=True) if phone_el else ''
    if not phone:
        # check for phone in contact-row
        for div in soup.find_all('div', class_=lambda c: c and 'phone' in c):
            phone = div.get_text(strip=True)
            break
            
    print(f"{asurite} -> Office: '{street}' | Campus/City: '{city or campus}' | Mail: '{mail_code}' | Phone: '{phone}'")
