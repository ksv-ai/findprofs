import cloudscraper
import urllib.parse
import json

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# In the HTML we saw:
# data-searchtype="departments"
# data-depts="1662"
# data-employeetype="Faculty,Faculty w/Admin Appointment"
# data-exclude="bakerd,hbryan,fegarret,..."

params = {
    "dept_ids": "1662",
    "employee_types": "Faculty,Faculty w/Admin Appointment",
    "size": "100",
    "page": "1"
}
url = "https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered?" + urllib.parse.urlencode(params)
r = scraper.get(url)
print("Status:", r.status_code)
data = r.json()
print("Total results:", data.get("meta", {}).get("page", {}).get("total_results"))
print("Total pages:", data.get("meta", {}).get("page", {}).get("total_pages"))

# Sample faculty members
for item in data.get("results", [])[:10]:
    name = item.get("display_name", {}).get("raw")
    email = item.get("email_address", {}).get("raw")
    title = item.get("primary_title", {}).get("raw", [""])[0] if item.get("primary_title", {}).get("raw") else ""
    asurite = item.get("asurite_id", {}).get("raw")
    bio = item.get("short_bio", {}).get("raw") or item.get("bio", {}).get("raw") or ""
    expertise = item.get("expertise_areas", {}).get("raw") or []
    interests = item.get("research_interests", {}).get("raw") or ""
    print(f"- {name} | {title} | {email} | asurite: {asurite}")
    if expertise or interests:
        print(f"    Expertise/Interests: {expertise} | {str(interests)[:100]}")
