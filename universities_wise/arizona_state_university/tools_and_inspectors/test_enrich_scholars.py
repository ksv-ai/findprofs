import cloudscraper
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "desktop": True})

# Known manual map for faculty whose scholar profiles are verified
VERIFIED_SCHOLAR = {
    "Kangping Chen": {"id": "xT-lX9sAAAAJ", "citations": 3523},
    "Alberto Scotti": {"id": "HRx2lJQAAAAJ", "citations": None},
    "Marcus Herrmann": {"id": "yv6aCW8AAAAJ", "citations": None},
    "Yulia Peet": {"id": "_6o8MrUAAAAJ", "citations": None},
    "Kiran Ramesh": {"id": "DKc-AgcAAAAJ", "citations": None},
    "Aditi Chattopadhyay": {"id": "w3fU9E0AAAAJ", "citations": None},
    "Leixin Ma": {"id": "2xQTOc0AAAAJ", "citations": None},
    "Kunal Garg": {"id": "vs3pl-8AAAAJ", "citations": None},
    "Beomjin Kwon": {"id": "fs2d97sAAAAJ", "citations": None},
    "Cindy (Xiangjia) Li": {"id": "tGQzHJIAAAAJ", "citations": None},
    "Hamidreza Marvi": {"id": "00Fepb0AAAAJ", "citations": None},
    "Houlong Zhuang": {"id": "4yYKCpUAAAAJ", "citations": None},
    "Huan Wu": {"id": "8CS4X9IAAAAJ", "citations": None},
    "Jagannathan Rajagopalan": {"id": "ClqRIhIAAAAJ", "citations": None},
    "Jiefeng Sun": {"id": "fjUoHOsAAAAJ", "citations": None},
    "Konrad Rykaczewski": {"id": "SWeAf4UAAAAJ", "citations": None},
    "Minglei Qu": {"id": "9LWNC50AAAAJ", "citations": None},
    "Robert Wang": {"id": "LaUdx9gAAAAJ", "citations": None},
    "Spring Berman": {"id": "KKup0OgAAAAJ", "citations": None},
    "Wanxin Jin": {"id": "SoEC4h4AAAAJ", "citations": None},
    "Wonmo Kang": {"id": "bHyyOTAAAAAJ", "citations": None},
}

# OpenAlex lookup for citations as fallback/cross-check
def get_openalex_citations(name):
    try:
        url = "https://api.openalex.org/authors"
        params = {"search": f"{name} Arizona State University", "mailto": "Feenday1964@cuvox.de", "api_key": "NzjuLll4FIEV5HFS2mCK4g"}
        r = requests.get(url, params=params, timeout=8)
        if r.status_code == 200:
            res = r.json().get("results", [])
            if res:
                return res[0].get("cited_by_count")
    except Exception:
        pass
    return None

print("Fetching citations for sample verified scholars...")
for name, data in list(VERIFIED_SCHOLAR.items())[:5]:
    openalex_cites = get_openalex_citations(name)
    print(f"{name} -> Scholar ID: {data['id']}, OpenAlex Citations: {openalex_cites}")
