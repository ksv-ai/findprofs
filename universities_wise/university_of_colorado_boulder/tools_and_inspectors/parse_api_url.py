import cloudscraper
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
js_url = "https://faculty.engineering.asu.edu/directory/wp-content/plugins/pitchfork-people/src/app-webdir-ui/js/webdirUI.umd.js"
r = scraper.get(js_url)

idx = r.text.find("let E=`${e.API_URL")
if idx != -1:
    print(r.text[idx:idx+1000])
