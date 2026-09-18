from scholarly import scholarly

try:
    author = scholarly.search_author_id('HRx2lJQAAAAJ')
    print("Found author by ID:")
    print("Name:", author['name'])
    print("Affiliation:", author['affiliation'])
    print("Citedby:", author.get('citedby'))
    print("Scholar ID:", author.get('scholar_id'))
    print("Interests:", author.get('interests'))
except Exception as e:
    import traceback
    traceback.print_exc()
