import cloudscraper
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
url = "https://search.asu.edu/profile/mherrma1"
r = scraper.get(url)
print("Length:", len(r.text))
m1 = re.findall(r'scholar\.google\.com/citations\?[^"\'\s<>]+user=([a-zA-Z0-9_-]{12})', r.text)
m2 = re.findall(r'user=([a-zA-Z0-9_-]{12})', r.text)
print("m1:", m1)
print("m2:", m2)
