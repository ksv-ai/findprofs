import requests
import json

# OpenAlex author search for Marcus Herrmann at ASU
url = "https://api.openalex.org/authors"
params = {
    "search": "Marcus Herrmann",
    "filter": "affiliations.institution.id:I57206974" # ASU institution id or search
}
r = requests.get(url, params={"search": "Marcus Herrmann Arizona State University"})
data = r.json()
print("OpenAlex results count:", len(data.get("results", [])))
if data.get("results"):
    author = data["results"][0]
    print("Name:", author.get("display_name"))
    print("ID:", author.get("id"))
    print("ORCID:", author.get("orcid"))
    print("IDS:", author.get("ids"))
