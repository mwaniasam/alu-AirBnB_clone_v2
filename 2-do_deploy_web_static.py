#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.
"""
from fabric.api import env, put, run
from os.path import exists
import os
import re

# Set Fabric environment variables
env.user = "ubuntu"
env.hosts = ["100.27.221.227", "44.220.133.229"]
env.key_filename = '~/.ssh/id_rsa'


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
        folder_name = "/data/web_static/releases/{}".format(filename.split('.')[0])

        # Upload archive to /tmp/ on the web server
        put(archive_path, "/tmp/{}".format(filename))

        # Ensure the release folder exists
        run("mkdir -p {}".format(folder_name))

        # Extract archive and clean up
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))

        # Update symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))

        # Ensure Nginx serves the new version
        run("sudo mkdir -p /var/www/html/hbnb_static")
        run("sudo cp -r /data/web_static/current/* /var/www/html/hbnb_static/")

        print("Deployment successful!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
