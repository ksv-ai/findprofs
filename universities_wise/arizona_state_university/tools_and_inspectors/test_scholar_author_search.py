import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# In the user screenshot, we clearly see:
# "Kang Ping Chen"
# "Arizona State University"
# "Cited by 3523"
# "fluid mechanics petroleum engineering porous media flow pore pressure prediction"
# Notice that this matches the author search result on Google Scholar!

def search_scholar_author(name, university="Arizona State University"):
    q = f"{name} {university}"
    url = f"https://scholar.google.com/citations?view_op=search_authors&mauthors={urllib.parse.quote(q)}&hl=en"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        # Check if we got author card
        # Regex for Cited by and user ID
        # user id: /citations?user=([a-zA-Z0-9_-]+)
        # cited by: Cited by (\d+)
        user_m = re.search(r'href=["\']/citations\?user=([a-zA-Z0-9_-]+)', r.text)
        cited_m = re.search(r'Cited by\s*(\d+)', r.text, re.IGNORECASE)
        user_id = user_m.group(1) if user_m else None
        cited_by = int(cited_m.group(1)) if cited_m else None
        return user_id, cited_by
    except Exception as e:
        return None, None

test_profs = ["Kangping Chen", "Alberto Scotti", "Marcus Herrmann", "Aditi Chattopadhyay", "Kiran Ramesh"]
for p in test_profs:
    uid, cites = search_scholar_author(p)
    print(f"{p} -> User ID: {uid}, Total Citations: {cites}")
    time.sleep(1)
