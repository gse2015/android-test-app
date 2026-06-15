#!/usr/bin/env python3
import os
import subprocess
import json
import urllib.request
import sys

# Read token from env file
token = None
with open('/home/gse/.hermes/.env', 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('GITHUB_TOKEN=***') and not line.startswith('#'):
            token = line.split('=', 1)[1]
            break

if not token or len(token) < 10:
    print("ERROR: Could not read GITHUB_TOKEN")
    sys.exit(1)

print(f"Token loaded (length={len(token)}, prefix={token[:8]})")

# Step 1: Create repo via API
print("\n=== Step 1: Create GitHub repo ===")
req = urllib.request.Request(
    'https://api.github.com/user/repos',
    data=json.dumps({'name': 'android-test-app', 'auto_init': False}).encode(),
    headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    },
    method='POST'
)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        print(f"Repo created: {result.get('html_url', 'unknown')}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if 'already exists' in body:
        print("Repo already exists - OK")
    else:
        print(f"HTTP Error {e.code}: {body[:200]}")
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Step 2: Push code
print("\n=== Step 2: Push code ===")
os.chdir('/home/gse/android-test-app')

# Remove old remote if exists
subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)

# Add remote with token
remote_url = f'https://{token}@github.com/gse2015/android-test-app.git'
result = subprocess.run(['git', 'remote', 'add', 'origin', remote_url], capture_output=True, text=True)
if result.returncode != 0:
    print(f"Remote add failed: {result.stderr}")

# Push
result = subprocess.run(['git', 'push', '-u', 'origin', 'master'], capture_output=True, text=True, timeout=60)
print(f"Push stdout: {result.stdout}")
if result.stderr:
    print(f"Push stderr: {result.stderr}")
if result.returncode != 0:
    print("Push failed!")
    sys.exit(1)
print("Push successful!")

# Step 3: Create and push tag
print("\n=== Step 3: Create tag v1.0.0 ===")
subprocess.run(['git', 'tag', 'v1.0.0'], capture_output=True)
result = subprocess.run(['git', 'push', 'origin', 'v1.0.0'], capture_output=True, text=True, timeout=60)
print(f"Tag push stdout: {result.stdout}")
if result.stderr:
    print(f"Tag push stderr: {result.stderr}")
if result.returncode != 0:
    print("Tag push failed!")
    sys.exit(1)

print("\n=== All done! ===")
print("Check: https://github.com/gse2015/android-test-app/actions")
