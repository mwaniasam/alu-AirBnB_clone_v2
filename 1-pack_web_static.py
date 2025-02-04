#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    - Creates a `versions` directory if it doesn't exist.
    - The archive name is in the format:
      `web_static_<year><month><day><hour><minute><second>.tgz`.
    - The archive contains all files inside `web_static`.

    Returns:
        str: The archive path if successful, otherwise None.
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"versions/web_static_{timestamp}.tgz"

        local(f"tar -cvzf {archive_name} web_static")

        return archive_name
    except Exception:
        return None
