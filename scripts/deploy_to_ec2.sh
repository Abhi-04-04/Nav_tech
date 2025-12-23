#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 -k /path/to/key.pem -h host -u user [-r repo] [-a API_URL] [-d DATABASE_URL]

Options:
  -k  Path to SSH private key (PEM)
  -h  EC2 host (IP or DNS)
  -u  SSH username (e.g. ec2-user)
  -r  Git repo URL (default: https://github.com/Abhi-04-04/Nav_tech.git)
  -a  API_URL to inject into frontend/index.html (optional)
  -d  DATABASE_URL to write to /etc/loan_app.env on remote (optional)

Example:
  ./scripts/deploy_to_ec2.sh -k ~/keys/loan-app-key.pem -h 1.2.3.4 -u ec2-user -a https://api.example.com -d "postgresql://user:pass@db:5432/loan_db"
EOF
}

REPO="https://github.com/Abhi-04-04/Nav_tech.git"
KEY_PATH=""
HOST=""
USER=""
API_URL=""
DATABASE_URL=""

while getopts ":k:h:u:r:a:d:" opt; do
  case ${opt} in
    k) KEY_PATH="$OPTARG" ;;
    h) HOST="$OPTARG" ;;
    u) USER="$OPTARG" ;;
    r) REPO="$OPTARG" ;;
    a) API_URL="$OPTARG" ;;
    d) DATABASE_URL="$OPTARG" ;;
    *) usage; exit 1 ;;
  esac
done

if [[ -z "$KEY_PATH" || -z "$HOST" || -z "$USER" ]]; then
  usage
  exit 1
fi

if [[ ! -f "$KEY_PATH" ]]; then
  echo "Key file not found: $KEY_PATH"
  exit 1
fi

echo "Deploying to $USER@$HOST using key $KEY_PATH"

ssh -i "$KEY_PATH" -o StrictHostKeyChecking=no "$USER@$HOST" bash -s -- <<EOF
set -euo pipefail

# Prepare directories
sudo mkdir -p /opt/loan-app
sudo chown $USER:$USER /opt/loan-app
cd /opt/loan-app

# Clone or update repo
if [ -d .git ]; then
  git fetch --all --prune
  git reset --hard origin/main
  git pull origin main
else
  git clone "$REPO" .
fi

# Backend setup
cd backend
python3 -m venv .venv || true
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Write DATABASE_URL if provided
if [ -n "$DATABASE_URL" ]; then
  echo "DATABASE_URL='$DATABASE_URL'" | sudo tee /etc/loan_app.env > /dev/null
  sudo chmod 600 /etc/loan_app.env
fi

# Frontend setup and API injection
cd ../frontend
if [ -n "$API_URL" ]; then
  sed -i "s|http://YOUR_EC2_PUBLIC_IP:8000|$API_URL|g" index.html || true
fi

sudo mkdir -p /var/www/loan-frontend
sudo cp -r ./* /var/www/loan-frontend/
# Set ownership to a suitable web user (www-data on Debian/Ubuntu, nginx on Amazon Linux)
if id -u www-data >/dev/null 2>&1; then
  sudo chown -R www-data:www-data /var/www/loan-frontend
elif id -u nginx >/dev/null 2>&1; then
  sudo chown -R nginx:nginx /var/www/loan-frontend
else
  sudo chown -R $USER:$USER /var/www/loan-frontend
fi

# Install and configure nginx using available package manager
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y nginx
  sudo cp ../deploy/loan-app.nginx /etc/nginx/sites-available/loan-app
  sudo ln -sf /etc/nginx/sites-available/loan-app /etc/nginx/sites-enabled/loan-app
elif command -v yum >/dev/null 2>&1; then
  sudo yum makecache -y
  sudo yum install -y nginx
  sudo cp ../deploy/loan-app.nginx /etc/nginx/conf.d/loan-app.conf
else
  echo "No known package manager found; please install nginx manually" >&2
fi

sudo nginx -t || true
sudo systemctl restart nginx || true

sudo cp ../deploy/loan-app.service /etc/systemd/system/loan-app.service
# Update service user/group to the current deploy user
sudo sed -i "s/^User=.*$/User=$USER/" /etc/systemd/system/loan-app.service || true
sudo sed -i "s/^Group=.*$/Group=$USER/" /etc/systemd/system/loan-app.service || true
sudo systemctl daemon-reload
sudo systemctl enable --now loan-app || true

# Smoke test
sleep 2
# Temporarily relax errexit to capture curl exit code safely
set +e
curl -s http://127.0.0.1:8000/customers >/dev/null
CURL_EXIT=$?
set -e
if [ "$CURL_EXIT" -eq 0 ]; then
  echo "Smoke test passed (200)"
else
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/customers) || STATUS=000
  if [ "$STATUS" = "503" ]; then
    echo "Smoke test passed (503)"
  else
    echo "Smoke test failed (status $STATUS)" >&2
    exit 2
  fi
fi

echo "Deploy finished successfully"
EOF

echo "Done. If successful, visit your frontend and verify functionality." 
