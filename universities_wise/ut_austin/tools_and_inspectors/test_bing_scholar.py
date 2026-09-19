import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def find_scholar_id_bing(name, university="Arizona State University"):
    q = f'"{name}" "{university}" "citations?user="'
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    r = requests.get(url, headers=headers, timeout=10)
    m = re.search(r'scholar\.google\.com/citations\?user=([a-zA-Z0-9_-]{12})', r.text)
    if m:
        return m.group(1)
    return None

test_names = ["Marcus Herrmann", "Yulia Peet", "Kiran Ramesh", "Jeonglae Kim", "Alberto Scotti", "Aditi Chattopadhyay", "Leixin Ma"]
for n in test_names:
    uid = find_scholar_id_bing(n)
    print(f"{n} -> {uid}")
