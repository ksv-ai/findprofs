import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
url = "https://faculty.engineering.asu.edu/directory/semte/aerospace-and-mechanical-engineering/"
r = scraper.get(url)
soup = BeautifulSoup(r.text, "lxml")
div = soup.find(class_="pfpeople-web-directory")
for k, v in div.attrs.items():
    print(f"{k}: {v}\n")
