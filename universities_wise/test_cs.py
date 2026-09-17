import cloudscraper
import time

for delay in [1, 2]:
    for interp in ['native', 'js2py', 'nodejs']:
        try:
            cs = cloudscraper.create_scraper(
                interpreter=interp,
                delay=delay,
                browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
            )
            r = cs.get('https://aero.engin.umich.edu/people/')
            print(f"interp={interp} delay={delay} -> {r.status_code}")
            if r.status_code == 200:
                print("SUCCESS with", interp, delay)
                break
        except Exception as e:
            print(f"interp={interp} error: {e}")
