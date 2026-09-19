import subprocess
import urllib.request
import json

proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
stdout, _ = proc.communicate(input='protocol=https\nhost=github.com\n')
token = None
for line in stdout.splitlines():
    if line.startswith('password='):
        token = line.split('=', 1)[1].strip()

if not token:
    print("No token found")
    exit(1)

req = urllib.request.Request(
    'https://api.github.com/user/repos?per_page=100',
    headers={'Authorization': f'Bearer {token}', 'User-Agent': 'Python'}
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("User repos:")
        for r in data:
            print(f"- {r['full_name']} (private: {r['private']})")
except Exception as e:
    print("Error:", e)
