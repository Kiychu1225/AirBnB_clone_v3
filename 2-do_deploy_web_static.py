#!/usr/bin/python3
"""
Fabric script that deploys an archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_extension))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_extension))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_extension))
        run('rm -rf {}{}/web_static'.format(path, no_extension))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_extension))
        return True
    except Exception:
        return False

