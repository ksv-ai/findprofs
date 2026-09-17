import cloudscraper
import time

cs = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
cs.get('https://aero.engin.umich.edu/')
time.sleep(1)
for filter_url in [
    'https://aero.engin.umich.edu/people/?fwp_roles=faculty',
    'https://aero.engin.umich.edu/people/?fwp_roles=core-faculty',
    'https://aero.engin.umich.edu/people/?query-19-filter=faculty'
]:
    r = cs.get(filter_url)
    print(filter_url, '->', r.status_code, 'len:', len(r.text))
