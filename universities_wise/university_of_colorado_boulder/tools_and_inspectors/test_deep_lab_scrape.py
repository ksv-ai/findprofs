import cloudscraper
from bs4 import BeautifulSoup
import re
import time
import urllib.parse

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})
scraper.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})

test_labs = [
    ("Mohamed Houssem Kasbaoui", "https://kasbaoui.bitbucket.io"),
    ("Kunal Garg", "https://sites.google.com/asu.edu/kunalgarg/"),
    ("Jiefeng Sun", "https://sunroboticslab.github.io"),
    ("Matthew Peet", "http://control.asu.edu/"),
    ("Liping Wang", "http://faculty.engineering.asu.edu/lpwang"),
    ("Leixin Ma", "https://sites.google.com/view/oasislabasu"),
    ("Spring Berman", "http://faculty.engineering.asu.edu/acs/"),
    ("Konrad Rykaczewski", "http://faculty.engineering.asu.edu/konrad/"),
    ("Wanxin Jin", "https://irislab.tech/"),
    ("Ronald Calhoun", "https://windlab.engineering.asu.edu/ronald-calhoun/"),
]

def analyze_lab(name, url):
    data = {
        "Hiring Status": "",
        "Required Skills / Prereqs": "",
        "Funding Sponsors": "",
        "Software / Code Repo": "",
        "Team Summary": "",
        "Latest Project / Highlight": ""
    }
    if not url or not url.startswith("http"):
        return data

    try:
        r = scraper.get(url, timeout=12)
        if r.status_code != 200:
            return data
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(separator=" ")
        
        # 1. Check hiring / openings
        hiring_indicators = []
        if any(w in text.lower() for w in ["looking for motivated", "openings", "join us", "open position", "phd positions available", "prospective students"]):
            # look for sentences mentioning students/openings
            sentences = re.split(r'[.\n]', text)
            for s in sentences:
                s_clean = " ".join(s.split())
                if any(k in s_clean.lower() for k in ["looking for", "openings", "positions available", "join our group", "join the lab"]) and len(s_clean) < 150:
                    hiring_indicators.append(s_clean)
                    break
            if hiring_indicators:
                data["Hiring Status"] = hiring_indicators[0]
            else:
                data["Hiring Status"] = "Actively recruiting / Openings mentioned on site"

        # 2. Check for Code / GitHub Repos
        gh_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "github.com" in href or "bitbucket.org" in href or "gitlab.com" in href:
                if not any(ign in href for sign in ["github.com/google", "github.com/facebook"] for ign in [sign]):
                    gh_links.add(href)
        if gh_links:
            data["Software / Code Repo"] = ", ".join(list(gh_links)[:2])

        # 3. Check for Funding Sponsors
        sponsors = set()
        for sp in ["NSF", "NASA", "DARPA", "ONR", "AFOSR", "DOE", "NIH", "ARPA-E", "Lockheed", "Boeing", "Honeywell", "Sandia"]:
            pattern = r'\b' + sp + r'\b'
            if re.search(pattern, text):
                sponsors.add(sp)
        if sponsors:
            data["Funding Sponsors"] = ", ".join(sorted(list(sponsors)))

        # 4. Check for Team count
        team_matches = re.findall(r'(\d+)\s*(?:phd|ph\.d|postdoc|graduate|undergraduate)\s*students?', text, re.I)
        if team_matches:
            data["Team Summary"] = f"{team_matches[0]} researchers/students mentioned"

        # 5. Extract latest project / highlight from headings
        headings = [h.get_text(strip=True) for h in soup.find_all(['h2', 'h3', 'h4']) if len(h.get_text(strip=True)) > 8 and len(h.get_text(strip=True)) < 80]
        if headings:
            data["Latest Project / Highlight"] = headings[0]

    except Exception as e:
        pass
    return data

for name, url in test_labs:
    res = analyze_lab(name, url)
    print(f"=== {name} ({url}) ===")
    for k, v in res.items():
        if v:
            print(f"  {k}: {v}")
    print()
