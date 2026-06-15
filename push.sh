#!/bin/bash
export GITHUB_TOKEN=*** "^GITHUB_TOKEN=*** /home/gse/.hermes/.env | head -1 | cut -d= -f2- | tr -d '\n\r')

# Create repo
echo "Creating repo..."
curl -s --connect-timeout 10 -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"android-test-app","auto_init":false}'

echo ""
echo "=== Repo created ==="

# Add remote and push
cd /home/gse/android-test-app
git remote remove origin 2>/dev/null
git remote add origin https://$GITHUB_TOKEN@github.com/gse2015/android-test-app.git
git push -u origin master

echo "=== Push done ==="
echo "Creating tag v1.0.0..."
git tag v1.0.0
git push origin v1.0.0

echo "=== Tag pushed ==="
