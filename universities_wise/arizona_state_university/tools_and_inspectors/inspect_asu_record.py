import cloudscraper
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
url = "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered?dept_ids=1662&size=2"
r = scraper.get(url)
data = r.json()
print("Meta:", data.get("meta"))
print("\nSample result 0:")
print(json.dumps(data["results"][0], indent=2))
