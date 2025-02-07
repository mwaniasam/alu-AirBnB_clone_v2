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
    Generates a .tgz archive from the web_static directory.

    Returns:
        str: Archive path if successful, None otherwise.
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
    Full deployment: Creates an archive and deploys it.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """

    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
