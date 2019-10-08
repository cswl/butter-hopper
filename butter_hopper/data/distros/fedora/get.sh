#!/bin/bash

RELEASE_VER="$1"

curl -L -o "/tmp/fedora-29.rootfs.xz"  "https://download.fedoraproject.org/pub/fedora/linux/releases/${RELEASE_VER}/Cloud/x86_64/images/Fedora-Cloud-Base-29-1.2.x86_64.raw.xz"