import requests
import json

# Fetch detail for https://openalex.org/A5009928604
r = requests.get("https://api.openalex.org/authors/A5009928604")
data = r.json()
print("Author keys:", data.keys())
print("IDs:", json.dumps(data.get("ids"), indent=2))
