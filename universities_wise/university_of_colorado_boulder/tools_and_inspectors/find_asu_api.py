import cloudscraper

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Fetch the webdir js
js_url = "https://faculty.engineering.asu.edu/directory/wp-content/plugins/pitchfork-people/dist/js/app-webdir-init.js"
r = scraper.get(js_url)
print("app-webdir-init.js status:", r.status_code)
print(r.text[:500])

js_url2 = "https://faculty.engineering.asu.edu/directory/wp-content/plugins/pitchfork-people/src/app-webdir-ui/js/webdirUI.umd.js"
r2 = scraper.get(js_url2)
print("webdirUI.umd.js status:", r2.status_code)
# look for api urls in the js
import re
apis = re.findall(r'https?://[^\s"\'`)]+', r2.text)
print("APIs found in webdirUI:")
for a in set(apis):
    if any(k in a.lower() for k in ["asu", "api", "search", "people"]):
        print(a)
