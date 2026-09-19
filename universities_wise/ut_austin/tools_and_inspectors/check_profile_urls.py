import cloudscraper
import urllib.parse
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Test pulling asurite search for faculty
r = scraper.get("https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered?dept_ids=1662&employee_types=Faculty,Faculty%20w/Admin%20Appointment&size=10")
for item in r.json().get("results", []):
    asurite = item.get("asurite_id", {}).get("raw")
    print(f"ASURITE: {asurite}")
    # Let's see what URLs work for faculty profile
    # https://faculty.engineering.asu.edu/directory/person/{asurite} or https://isearch.asu.edu/profile/{asurite} or https://search.asu.edu/profile/{asurite}
    res_site = item.get("research_website", {}).get("raw")
    site = item.get("website", {}).get("raw")
    print("  research_website:", res_site, "website:", site)
