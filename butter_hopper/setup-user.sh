#!/bin/bash 

usereuid="$1"
username="$2"

if [ -z "$usereuid" ] ; then 
    echo "No args provided."
    exit 0
fi

DEB_GROUPS="users,sudo,adm,cdrom,sudo,dip,plugdev"
FED_GROUPS="wheel,users"

setup_user_group() {
    useradd -m -u "$usereuid" -G  "$FED_GROUPS" "$username" 
}

setup_user_group
passwd "$username"