import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    url = "https://scholar.google.com/citations?view_op=search_authors&mauthors=Kang+Ping+Chen+Arizona+State+University&hl=en"
    await page.goto(url)
    content = await page.content()
    print("Page title:", await page.title())
    print("Length:", len(content))
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
