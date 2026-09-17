from bs4 import BeautifulSoup

with open('umich_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'lxml')

pagination = soup.find(class_=lambda c: c and 'pagination' in c.lower())
print("Pagination found:", bool(pagination))
if pagination:
    for a in pagination.find_all('a', href=True):
        print("  Page link:", a.text.strip(), a['href'])

# Also check any page links
page_links = soup.find_all('a', href=lambda h: h and '/page/' in h)
print("Page links count:", len(page_links))
for pl in page_links:
    print("  Link:", pl.text.strip(), pl['href'])
