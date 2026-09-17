import requests
import json

API_KEY = 'NzjuLll4FIEV5HFS2mCK4g'
session = requests.Session()
session.params = {'api_key': API_KEY, 'mailto': 'Feenday1964@cuvox.de'}

# Test Stanford
r = session.get('https://api.openalex.org/institutions', params={'search': 'Stanford University', 'filter': 'country_code:us', 'per-page': 1})
inst = r.json()['results'][0]
inst_id = inst['id'].split('/')[-1]
print('Resolved Stanford:', inst['display_name'], inst_id, inst.get('homepage_url'))

search_query = 'CFD OR aerodynamics OR "fluid mechanics" OR turbulence OR hypersonics OR propulsion OR "scientific computing"'

works_r = session.get('https://api.openalex.org/works', params={
    'filter': f'institutions.id:{inst_id},publication_year:2022-2026',
    'search': search_query,
    'group_by': 'authorships.author.id',
    'per-page': 5
})
authors = works_r.json().get('group_by', [])
print(f'Found {len(authors)} top authors at Stanford:')
for a in authors:
    print('  ', a.get('key_display_name'), '-> count:', a.get('count'))
