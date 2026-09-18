import cloudscraper
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
js_url = "https://faculty.engineering.asu.edu/directory/wp-content/plugins/pitchfork-people/src/app-webdir-ui/js/webdirUI.umd.js"
r = scraper.get(js_url)

# find where e.url is passed or configured
matches = re.findall(r'url\s*:\s*[`\'"][^`\'"]+[`\'"]', r.text)
print("url properties in webdirUI:", set(matches))
