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
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-security main restricted universe multiverse
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-updates main restricted universe multiverse
deb [arch=amd64] file:///media/{username}/apt-mirror/mirror/ca.archive.ubuntu.com/ubuntu xenial-backports main restricted universe multiverse

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


def backup_thidrparty_sourcelist(filename):
    print('backing up third party sourcelist')
    run = subprocess.run(['tar', '-zcvf', filename, '/etc/apt/sources.list.d'])
    if (run.returncode == 0):
        print('Third party sourcelist is backed up in ' +
              filename)
        return 0
    else:
        raise Exception('Cannot set permissions for apt')


def remove_thirdparty_sourcelist():
    # get file list
    mypath = '/etc/apt/sources.list.d/'
    try:
        (_, _, files) = next(os.walk(mypath))
    except Exception:
        return 0

    files = map(lambda f: mypath + f, files)
    files = [f for f in files]

    if len(files) == 0:
        return 0

    run = subprocess.run(['sudo', 'rm'] + files)
    if (run.returncode == 0):
        print('Remove third party sourcelist')
        return 0
    else:
        raise Exception('Cannot remove thirdparty sourcelist')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--dmz',
        dest='dmz',
        const='184.71.215.45/r4.5/amd64',
        nargs='?',
        type=str,
        default=False,
        help='Add mirror server address')

    parser.add_argument(
        '-u',
        '--usb',
        dest='usb',
        action='store_true',
        help='Install offline usb mirror')

    args = parser.parse_args()

    sourcefile = '/tmp/ivt-http-mirror.list'

    username = os.environ['USER']
    mirror_path = '/media/' + username + '/apt-mirror'

    sourcefile_offline = '/tmp/ivt-offline-mirror.list'
    default_source = 'sources.list'

    backup_file = os.environ['HOME'] + '/third-party-sourcelist.gz.tar'

    if (not args.dmz and not args.usb):
        parser.print_help()
        sys.exit(0)

    try:
        backup_thidrparty_sourcelist(backup_file)
        remove_thirdparty_sourcelist()
        if args.dmz:
            sourcefile = copy_to_temp(sourcefile, args.dmz)
            copy_to_source_list(sourcefile)
            print('IVT http mirror added successfully')

        if args.usb:
            is_mirror_available(mirror_path)
            allow_apt_access_user_media('/media/' + username)
            sourcefile_offline = copy_to_temp_offline(sourcefile_offline, username)
            copy_to_source_list(sourcefile_offline)
            print('IVT offline mirror added successfully')

        clear_default_source_list(default_source)

        sys.exit(0)

    except Exception as e:
        print('IVT mirror failed to added')
        print(e)
        sys.exit(1)
