import requests

API_KEY = 'NzjuLll4FIEV5HFS2mCK4g'
session = requests.Session()
session.params = {'api_key': API_KEY, 'mailto': 'Feenday1964@cuvox.de'}

terms = [
    'Aerospace engineering',
    'Mechanical engineering',
    'Applied mathematics',
    'Computational physics',
    'Aerodynamics',
    'Turbulence',
    'Propulsion',
    'Combustion',
    'Heat transfer',
    'Scientific computing'
]

for t in terms:
    r = session.get('https://api.openalex.org/concepts', params={'search': t}).json()
    if r.get('results'):
        c = r['results'][0]
        cid = c.get('id').split('/')[-1]
        name = c.get('display_name')
        print(f"{name:<35} -> {cid}")
