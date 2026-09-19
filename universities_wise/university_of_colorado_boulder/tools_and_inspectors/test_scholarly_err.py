from scholarly import scholarly
import traceback

try:
    search_query = scholarly.search_author('Kang Ping Chen')
    author = next(search_query)
    print(author)
except Exception as e:
    traceback.print_exc()
