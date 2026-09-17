import cloudscraper
import time

for attempt in range(1, 8):
    cs = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    # First visit homepage to get cookies/clearance
    r_home = cs.get('https://aero.engin.umich.edu/')
    time.sleep(1)
    r_people = cs.get('https://aero.engin.umich.edu/people/')
    print(f"Attempt {attempt}: home={r_home.status_code}, people={r_people.status_code}, title='{cs.get('https://aero.engin.umich.edu/people/').text[:150]}'")
    if r_people.status_code == 200 and 'Just a moment' not in r_people.text:
        print("Bypassed successfully!")
        with open('umich_page.html', 'w', encoding='utf-8') as f:
            f.write(r_people.text)
        break
    time.sleep(2)
