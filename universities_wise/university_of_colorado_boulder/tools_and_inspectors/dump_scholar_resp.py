import requests

url = "https://scholar.google.com/citations?view_op=search_authors&mauthors=Kang+Ping+Chen+Arizona+State+University&hl=en"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
r = requests.get(url, headers=headers)
print("Status:", r.status_code)
print(r.text[:500])
with open("C:/Users/Keshav/.gemini/antigravity-ide/brain/7bc76225-2bd9-4bac-991d-c022a4677b5f/scratch/scholar_response.html", "w", encoding="utf-8") as f:
    f.write(r.text)
print("Saved to scholar_response.html")
