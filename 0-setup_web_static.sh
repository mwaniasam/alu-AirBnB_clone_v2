#!/usr/bin/env bash
# Script to set up web servers for deployment of web_static

# Install Nginx
if ! command -v nginx &> /dev/null; then
    sudo apt update
    sudo apt install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a simple HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create (or update) the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Ensure ubuntu user/group owns everything under /data/
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve web_static
nginx_config="/etc/nginx/sites-available/default"

# Check if alias already exists, if not, add it
if ! grep -q "location /hbnb_static/" "$nginx_config"; then
    sudo sed -i '/server_name _;/a \
    location /hbnb_static/ { \
        alias /data/web_static/current/; \
        index index.html; \
    }' "$nginx_config"
fi

sudo systemctl restart nginx

exit 0
