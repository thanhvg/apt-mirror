#!/usr/bin/env python3

import os
import fileinput
import sys
import subprocess


def is_mirror_available(path):
    flag = os.path.exists(path)
    if (flag):
        return flag
    else:
        raise Exception('Mirror location not found')


def write_apt_sources(filename, string):
    try:
        with fileinput.FileInput(
                filename, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace('intelliview', string), end='')
        return
    except Exception as e:
        raise e


def copy_to_temp(filename):
    run = subprocess.run(['cp', filename, '/tmp/'])
    if (run.returncode == 0):
        return '/tmp/ivt-mirror.list'
    else:
        raise Exception('Cannot copy to tmp')


def copy_to_source_list(filename):
    run = subprocess.run(['sudo', 'cp', filename, '/etc/apt/sources.list.d/'])
    # run = subprocess.run(['sudo', 'cp', filename, '/home/gvuong/Documents'])

    if (run.returncode == 0):
        return 0
    else:
        raise Exception('Cannot copy to etc')


def allow_apt_access_user_media(path):
    run = subprocess.run(['sudo', 'setfacl', '-m', '_apt:rx', path])
    if (run.returncode == 0):
        return 0
    else:
        raise Exception('Cannot set permissions for apt')


if __name__ == '__main__':
    #  username = os.getlogin()
    username = os.environ['USER']
    mirror_path = '/media/' + username + '/apt-mirror'
    sourcefile = './src/sources.list.d/ivt-mirror.list'

    try:
        is_mirror_available(mirror_path)
        allow_apt_access_user_media('/media/' + username)

        if (username != 'intelliview'):
            sourcefile = copy_to_temp(sourcefile)
            write_apt_sources(sourcefile, username)

        copy_to_source_list(sourcefile)

        print('APP SUCCEEDED')
        sys.exit(0)

    except Exception as e:
        print('APP FAILED')
        print(e)
        sys.exit(1)
