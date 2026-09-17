import requests

API_KEY = 'NzjuLll4FIEV5HFS2mCK4g'
session = requests.Session()
session.params = {'api_key': API_KEY, 'mailto': 'Feenday1964@cuvox.de'}

inst_id = 'I97018004' # Stanford
SEARCH_TERMS = 'aerodynamics OR aerospace OR "fluid mechanics" OR turbulence OR combustion OR propulsion OR hypersonics OR "computational physics"'

broad = session.get('https://api.openalex.org/works', params={
    'filter': f'institutions.id:{inst_id},publication_year:2022-2026',
    'search': SEARCH_TERMS,
    'group_by': 'authorships.author.id',
    'per-page': 5
}).json()

groups = broad.get('group_by', [])
print('Found groups:', len(groups))
for g in groups:
    a_id = g['key'].split('/')[-1]
    name = g['key_display_name']
    works = session.get('https://api.openalex.org/works', params={
        'filter': f'author.id:{a_id},institutions.id:{inst_id},publication_year:2022-2026',
        'sort': 'cited_by_count:desc',
        'per-page': 5
    }).json().get('results', [])
    print(f'Author: {name} (ID: {a_id}) -> {len(works)} works')
    if works:
        print(f'   Paper: {works[0].get("title")}')
