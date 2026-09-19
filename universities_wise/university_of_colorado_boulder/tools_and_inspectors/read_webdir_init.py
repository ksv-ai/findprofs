import cloudscraper
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
js_url = "https://faculty.engineering.asu.edu/directory/wp-content/plugins/pitchfork-people/dist/js/app-webdir-init.js"
r = scraper.get(js_url)
print(r.text)
