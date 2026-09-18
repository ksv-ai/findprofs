import cloudscraper
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
js_url = "https://faculty.engineering.asu.edu/directory/wp-content/plugins/pitchfork-people/src/app-webdir-ui/js/webdirUI.umd.js"
r = scraper.get(js_url)

# Search for api paths in the JS
lines = [line for line in r.text.split(";") if any(k in line for k in ["api/v1", "web_dir", "deptIds", "searchType"])]
for l in lines[:10]:
    print("Found snippet:", l[:200])

matches = re.findall(r'[`\'"][^`\'"]*api/v1[^`\'"]*[`\'"]', r.text)
print("api/v1 patterns:", set(matches))
