#!/bin/bash

## boot strap any distro with boot crapper
## Runs your `debootstrap` `pacstrap` and `dnf --install root` 
## inside a secure namespaced container

ALPINE_DIR="$1"
BTRFS_SUBVOL="$2"
DISTRO="$3"

mount -t tmpfs tmpfs "$ALPINE_DIR/mnt"
mkdir "$ALPINE_DIR/mnt/bootcrapper"
mkdir "$ALPINE_DIR/mnt/new_root"

mount -o "subvol=$BTRFS_SUBVOL" 

systemd-nspawn -D "$ALPINE_DIR"  -a /bin/sh 