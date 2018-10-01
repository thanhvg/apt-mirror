#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse


def write_source_list(server):
    return  """
# main
deb [arch=amd64] http://{server}/ca.archive.ubuntu.com/ubuntu xenial main restricted universe multiverse

# node
# deb http://{server}/deb.nodesource.com/node_10.x xenial main

# google
deb [arch=amd64] http://{server}/dl.google.com/linux/chrome/deb/ stable main

# postgresql
deb http://{server}/apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
""".format(server=server)


def is_mirror_available(path):
    flag = os.path.exists(path)
    if (flag):
        return flag
    else:
        raise Exception('Mirror location not found')


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--server',
        dest='server',
        type=str,
        default='dmz-server',
        help='Mirror server address')
    args = parser.parse_args()

    server = args.server
    sourcefile = '/tmp/ivt-http-mirror.list'

    try:
        sourcefile = copy_to_temp(sourcefile, server)
        copy_to_source_list(sourcefile)
        print('IVT mirror added successfully')
        sys.exit(0)

    except Exception as e:
        print('IVT mirror failed to added')
        print(e)
        sys.exit(1)
