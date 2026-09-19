import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Test Alberto Scotti whose Scholar ID was found: HRx2lJQAAAAJ
# Test Kang Ping Chen (from user screenshot: cited by 3523)
# Test Marcus Herrmann: yv6aCW8AAAAJ

scholar_ids = ["HRx2lJQAAAAJ", "yv6aCW8AAAAJ", "_6o8MrUAAAAJ"]

for uid in scholar_ids:
    url = f"https://scholar.google.com/citations?user={uid}&hl=en"
    r = scraper.get(url)
    print(f"User {uid} status: {r.status_code}")
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "lxml")
        # Table of citations
        # <td class="gsc_rsb_std">All</td> or <td class="gsc_rsb_std">...</td>
        stats = soup.find_all("td", class_="gsc_rsb_std")
        if stats:
            total_citations = stats[0].get_text(strip=True)
            h_index = stats[2].get_text(strip=True) if len(stats) > 2 else ""
            i10_index = stats[4].get_text(strip=True) if len(stats) > 4 else ""
            print(f"  -> Total Citations: {total_citations}, h-index: {h_index}, i10-index: {i10_index}")
        else:
            # check regex
            m = re.search(r'Cited by</td><td class="gsc_rsb_std">(\d+)', r.text)
            print(f"  -> Regex match: {m.group(1) if m else 'None'}")
