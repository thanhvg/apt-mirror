#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def write_source_list(server):
    return """
# main
deb [arch=amd64] http://{server}/ca.archive.ubuntu.com/ubuntu xenial main restricted universe multiverse
deb [arch=amd64] http://{server}/ca.archive.ubuntu.com/ubuntu xenial-security main restricted universe multiverse
deb [arch=amd64] http://{server}/ca.archive.ubuntu.com/ubuntu xenial-updates main restricted universe multiverse
# deb [arch=amd64] http://{server}/ca.archive.ubuntu.com/ubuntu xenial-proposed main restricted universe multiverse
deb [arch=amd64] http://{server}/ca.archive.ubuntu.com/ubuntu xenial-backports main restricted universe multiverse

# node
# deb http://{server}/deb.nodesource.com/node_10.x xenial main

# google
deb [arch=amd64] http://{server}/dl.google.com/linux/chrome/deb/ stable main

# postgresql
deb http://{server}/apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
""".format(server=server)


def write_source_list_offline(username):
    return """
# main 
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial main restricted universe multiverse
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-security main restricted
# deb-src [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-security main restricted
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-security universe
# deb-src [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-security universe
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-security multiverse
# deb-src [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-security multiverse

# node
# deb file:///media/{username}/apt-mirror/mirror/deb.nodesource.com/node_10.x xenial main

# google
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/dl.google.com/linux/chrome/deb/ stable main

# postgresql
deb file:///media/{username}/apt-mirror/mirror/apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
""".format(username=username)


def is_mirror_available(path):
    flag = os.path.exists(path)
    if (flag):
        return flag
    else:
        raise Exception('Mirror location not found')

def copy_to_temp_offline(filename, username):
    content = write_source_list_offline(username)
    try:
        with open(filename, 'wt') as f:
            print(content, file=f)
        return filename
    except Exception:
        raise Exception('Cannot copy to tmp')

def copy_to_temp(filename, server):
    content = write_source_list(server)
    try:
        with open(filename, 'wt') as f:
            print(content, file=f)
        return filename
    except Exception:
        raise Exception('Cannot copy to tmp')


def copy_to_source_list(filename):
    run = subprocess.run(['sudo', 'cp', filename, '/etc/apt/sources.list.d/'])
    # run = subprocess.run(['cp', filename, '/home/gvuong/Documents'])

    if (run.returncode == 0):
        return 0
    else:
        raise Exception('Cannot copy to etc')


def clear_default_source_list(filename):

    file = open('/tmp/' + filename, 'w')
    file.write("# IVT mirror")
    file.close()

    run = subprocess.run(['sudo', 'cp', '/tmp/' + filename, '/etc/apt/'])

    if (run.returncode == 0):
        return 0
    else:
        raise Exception('Cannot clear default apt source')


def allow_apt_access_user_media(path):
    run = subprocess.run(['sudo', 'setfacl', '-m', '_apt:rx', path])
    if (run.returncode == 0):
        return 0
    else:
        raise Exception('Cannot set permissions for apt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--server',
        dest='server',
        type=str,
        default='184.71.215.45/r4.5/amd64',
        help='Mirror server address')
    args = parser.parse_args()

    server = args.server
    sourcefile = '/tmp/ivt-http-mirror.list'

    username = os.environ['USER']
    mirror_path = '/media/' + username + '/apt-mirror'

    sourcefile_offline = '/tmp/ivt-offline-mirror.list'
    default_source = 'sources.list'

    try:
        sourcefile = copy_to_temp(sourcefile, server)
        copy_to_source_list(sourcefile)
        print('IVT http mirror added successfully')

        is_mirror_available(mirror_path)
        allow_apt_access_user_media('/media/' + username)

        clear_default_source_list(default_source)

        sourcefile_offline = copy_to_temp_offline(sourcefile_offline, username)
        copy_to_source_list(sourcefile_offline)
        print('IVT offline mirror added successfully')

        sys.exit(0)

    except Exception as e:
        print('IVT mirror failed to added')
        print(e)
        sys.exit(1)
