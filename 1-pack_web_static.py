#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    # Create versions directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Generate timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{timestamp}.tgz"

    # Create the archive
    print(f"Packing web_static to {archive_name}")
    result = local(f"tar -cvzf {archive_name} web_static")

    # Return the archive path if successful, otherwise return None
    if result.succeeded:
        return archive_name
    else:
        return None
