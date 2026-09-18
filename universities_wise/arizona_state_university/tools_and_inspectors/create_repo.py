import subprocess
import urllib.request
import json

proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
stdout, _ = proc.communicate(input='protocol=https\nhost=github.com\n')
token = None
for line in stdout.splitlines():
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()

payload = json.dumps({
    "name": "findprofs",
    "description": "Scrape and find R1 universities faculty, research fields, and professor leads using OpenAlex and direct scrapers",
    "private": False
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.github.com/user/repos',
    data=payload,
    headers={
        'Authorization': f'Bearer {token}',
        'User-Agent': 'Python',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"Repository created successfully: {res.get('html_url')}")
except urllib.error.HTTPError as e:
    print(f"Error creating repo: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Unexpected error: {e}")
