import urllib.parse
import re
import cloudscraper
from bs4 import BeautifulSoup

def get_google_scholar_url(name: str, university: str = "") -> str:
    """
    Construct a direct, functional Google Scholar author URL.
    Points directly to the author citations search which routes straight
    to the author's public profile or author disambiguation card.
    """
    query = f"{name} {university}".strip()
    return f"https://scholar.google.com/citations?view_op=search_authors&mauthors={urllib.parse.quote(query)}"

print("Sample 1:", get_google_scholar_url("Alina Alexeenko", "Purdue University"))
print("Sample 2:", get_google_scholar_url("Carlos Cesnik", "University of Michigan"))
