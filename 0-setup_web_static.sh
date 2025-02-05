#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static.

# Install Nginx if not already installed
sudo apt-get update -y >/dev/null 2>&1
sudo apt-get install nginx -y >/dev/null 2>&1

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create (or update) the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of /data/ recursively
sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve content from /data/web_static/current/
NGINX_CONFIG="/etc/nginx/sites-available/default"

if ! grep -q "location /hbnb_static/" "$NGINX_CONFIG"; then
    sudo sed -i '51i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$NGINX_CONFIG"
fi

# Restart Nginx to apply changes
sudo service nginx restart

echo "Nginx setup complete. Web_static deployed!"
