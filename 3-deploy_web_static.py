#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
"""

from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists

# Set Fabric environment variables
env.user = "ubuntu"
env.hosts = ["100.27.221.227", "44.220.133.229"]
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """
    Creates a compressed archive of the web_static directory.

    This function:
    - Ensures the 'versions/' directory exists.
    - Creates a .tgz archive of 'web_static' with a timestamp.
    - Stores the archive in the 'versions/' folder.

    Returns:
        str: The path to the created archive if successful.
        None: If the archive creation fails.
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archive_path} web_static")

        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploys an archive to the web servers.

    This function:
    - Checks if the provided archive exists.
    - Uploads the archive to the /tmp/ directory on remote servers.
    - Extracts its content into a new release folder in /data/web_static/releases/.
    - Removes unnecessary files and directories.
    - Updates the symbolic link to point to the new deployment.

    Args:
        archive_path (str): The local path to the .tgz archive file.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not exists(archive_path):
        print("Error: Archive file does not exist.")
        return False

    try:
        filename = archive_path.split("/")[-1]
        folder_name = f"/data/web_static/releases/{filename.split('.')[0]}"

        # Upload archive
        put(archive_path, f"/tmp/{filename}")

        # Prepare deployment directory
        run(f"mkdir -p {folder_name}")
        run(f"tar -xzf /tmp/{filename} -C {folder_name}")
        run(f"rm /tmp/{filename}")
        run(f"mv {folder_name}/web_static/* {folder_name}")
        run(f"rm -rf {folder_name}/web_static")

        # Update symbolic link
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_name} /data/web_static/current")

        print("Deployment successful!")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False


def deploy():
    """
    Performs a full deployment by creating and distributing an archive.

    This function:
    - Calls do_pack() to generate a new archive.
    - If archive creation fails, it returns False.
    - Calls do_deploy() to upload and extract the archive on the servers.
    - Returns the result of do_deploy().

    Returns:
        bool: True if deployment succeeds, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
