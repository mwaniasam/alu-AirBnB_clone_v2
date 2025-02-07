#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.
"""

from fabric.api import env, put, run
from os.path import exists
import os

# Set Fabric environment variables
env.user = "ubuntu"
env.hosts = ["100.27.221.227", "44.220.133.229"]
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    Deploys the archive to the web servers.

    Args:
        archive_path (str): Path to the .tgz archive.

    Returns:
        bool: True if deployment succeeds, False otherwise.
    """
    if not exists(archive_path):
        print("Error: Archive file does not exist.")
        return False

    try:
        # Extract filename and folder name
        filename = os.path.basename(archive_path)
        folder_name = f"/data/web_static/releases/{filename.split('.')[0]}"

        # Upload archive to /tmp/ on the web server
        put(archive_path, f"/tmp/{filename}")

        # Ensure the release folder exists
        run(f"mkdir -p {folder_name}")

        # Extract archive and clean up
        run(f"tar -xzf /tmp/{filename} -C {folder_name}")
        run(f"rm /tmp/{filename}")
        run(f"mv {folder_name}/web_static/* {folder_name}")
        run(f"rm -rf {folder_name}/web_static")

        # Update symbolic link
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_name} /data/web_static/current")

        # Ensure Nginx serves the new version
        run("sudo mkdir -p /var/www/html/hbnb_static")
        run("sudo cp -r /data/web_static/current/* /var/www/html/hbnb_static/")

        print("Deployment successful!")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
