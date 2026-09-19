from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    url = "https://scholar.google.com/citations?view_op=search_authors&mauthors=Kang+Ping+Chen+Arizona+State+University&hl=en"
    page.goto(url)
    print("Page title:", page.title())
    content = page.content()
    print("Content length:", len(content))
    if "Cited by" in content:
        print("FOUND 'Cited by' in Playwright page!")
    browser.close()
