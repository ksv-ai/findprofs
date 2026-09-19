import subprocess
import urllib.request
import json

proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
stdout, _ = proc.communicate(input='protocol=https\nhost=github.com\n')
token = None
for line in stdout.splitlines():
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()

# Check user info and scopes
req = urllib.request.Request(
    'https://api.github.com/user',
    headers={'Authorization': f'Bearer {token}', 'User-Agent': 'Python'}
)

with urllib.request.urlopen(req) as resp:
    scopes = resp.headers.get('X-OAuth-Scopes', '')
    user = json.loads(resp.read().decode('utf-8'))
    print(f"Authenticated user: {user.get('login')}")
    print(f"Token scopes: {scopes}")

# Check if findprofs repo exists
req_repo = urllib.request.Request(
    'https://api.github.com/repos/ksv-ai/findprofs',
    headers={'Authorization': f'Bearer {token}', 'User-Agent': 'Python'}
)
try:
    with urllib.request.urlopen(req_repo) as resp:
        print("findprofs repo already exists!")
except urllib.error.HTTPError as e:
    print(f"findprofs repo status: {e.code}")
