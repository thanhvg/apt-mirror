#!/bin/bash
# -N is to update, drop -N to download all > 15 GB 
wget --no-parent -r -N http://apt.postgresql.org/pub/repos/apt/pool/ -P mirror/
wget --no-parent -r -N http://apt.postgresql.org/pub/repos/apt/dists/xenial-pgdg -P mirror/

# try this -m as sync 
# wget --no-parent -m -N http://apt.postgresql.org/pub/repos/apt/pool/ -P mirror/
# wget --no-parent -m -N http://apt.postgresql.org/pub/repos/apt/dists/xenial-pgdg -P mirror/
