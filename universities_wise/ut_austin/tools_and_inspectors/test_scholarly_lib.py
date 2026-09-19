from scholarly import scholarly

print("Testing scholarly author search for Kangping Chen...")
try:
    search_query = scholarly.search_author('Kang Ping Chen Arizona State University')
    author = next(search_query)
    print("Found author:", author['name'])
    print("Affiliation:", author['affiliation'])
    print("Scholar ID:", author['scholar_id'])
    print("Citedby:", author.get('citedby'))
    print("Interests:", author.get('interests'))
except Exception as e:
    print("Error:", e)
