import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Test DuckDuckGo HTML for Google Scholar user ID
def find_scholar_user_id(name, university="Arizona State University"):
    q = f'"{name}" "{university}" "scholar.google.com/citations?user="'
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    for a in soup.find_all("a", href=True):
        m = re.search(r'scholar\.google\.com/citations\?user=([a-zA-Z0-9_-]{12})', a['href'])
        if m:
            return m.group(1)
        # check url decoding of ddg redirect
        m2 = re.search(r'scholar\.google\.com%2Fcitations%3Fuser%3D([a-zA-Z0-9_-]{12})', a['href'])
        if m2:
            return m2.group(1)
    return None

test_names = ["Marcus Herrmann", "Yulia Peet", "Kiran Ramesh", "Jeonglae Kim", "Alberto Scotti"]
for n in test_names:
    uid = find_scholar_user_id(n)
    print(f"{n} -> {uid}")
