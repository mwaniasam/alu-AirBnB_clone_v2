#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt update -y
    sudo apt install nginx -y
fi

# Create necessary directories if they don’t exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create (or recreate) the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /hbnb_static/
sudo sed -i "/server_name _;/a location /hbnb_static/ { \
    alias /data/web_static/current/; \
    index index.html; \
}" /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart

# Exit successfully
exit 0
