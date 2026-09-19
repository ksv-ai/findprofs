import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()
sample_urls = [
    'https://kasbaoui.bitbucket.io',
    'https://sites.google.com/asu.edu/kunalgarg/',
    'https://sunroboticslab.github.io',
    'http://birth.asu.edu',
    'http://control.asu.edu/'
]

for url in sample_urls:
    try:
        r = scraper.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        nav = [a.get_text(strip=True) for a in soup.find_all('a') if len(a.get_text(strip=True)) > 2][:10]
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)][:8]
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        print(f"URL: {url} (Status {r.status_code})")
        print(f"  Title: {title}")
        print(f"  Headings: {headings[:6]}")
        print(f"  Navigation / Links: {nav[:6]}")
        print()
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
