import cloudscraper

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

test_urls = [
    "https://isearch.asu.edu/profile/kgarg24",
    "https://search.asu.edu/profile/kgarg24",
    "https://faculty.engineering.asu.edu/directory/person/kgarg24"
]

for u in test_urls:
    r = scraper.get(u, timeout=10)
    print(f"{u} -> {r.status_code} (final: {r.url})")
