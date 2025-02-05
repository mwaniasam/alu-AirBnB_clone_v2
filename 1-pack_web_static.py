#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of the AirBnB Clone repo.
"""
from fabric.api import local
from datetime import datetime
from os import makedirs


def do_pack():
    """
    Function to create a .tgz archive from web_static folder.
    Returns:
        str: Path to the created archive, or None if it fails.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    try:
        # Ensure the 'versions' directory exists
        makedirs("versions", exist_ok=True)

        # Create the archive
        result = local("tar -cvzf {} web_static".format(archive_path))

        if result.succeeded:
            return archive_path
        else:
            return None

    except Exception as e:
        print("Error: {}".format(e))
        return None
