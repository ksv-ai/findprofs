from bs4 import BeautifulSoup

with open('umich_page.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'lxml')

posts = soup.find_all(class_='wp-block-post')
print(f"Found {len(posts)} wp-block-post elements")

for p in posts[:5]:
    classes = p.get('class', [])
    # Name
    title_elem = p.find(class_='wp-block-post-title')
    name = title_elem.get_text(strip=True) if title_elem else "N/A"
    
    # Title / Position
    # Check paragraphs or custom fields inside post
    text_blocks = [t.get_text(strip=True) for t in p.find_all(['p', 'div', 'span']) if t.get_text(strip=True)]
    
    # Roles and Research Areas from classes!
    roles = [c.replace('role-', '') for c in classes if c.startswith('role-')]
    research = [c.replace('research-area-', '') for c in classes if c.startswith('research-area-')]
    
    # Email or link
    link_elem = p.find('a', href=True)
    link = link_elem['href'] if link_elem else ""
    
    email_elem = p.find('a', href=lambda h: h and 'mailto:' in h)
    email = email_elem['href'].replace('mailto:', '') if email_elem else ""

    print(f"Name: {name}")
    print(f"Classes: {classes}")
    print(f"Roles: {roles}")
    print(f"Research: {research}")
    print(f"Text blocks: {text_blocks}")
    print(f"Link: {link}, Email: {email}")
    print("-" * 50)
