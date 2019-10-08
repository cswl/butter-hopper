#!/bin/bash

function findSudoUser() {
    thisPID=$$
    origUser=$(whoami)
    thisUser=$origUser

    while [ "$thisUser" = "$origUser" ]
    do
        ARR=($(ps h -p$thisPID -ouser,ppid;))
        thisUser="${ARR[0]}"
        myPPid="${ARR[1]}"
        thisPID=$myPPid
    done

    getent passwd "$thisUser" | cut -d: -f1
}

current_uid=$(findSudoUser)

# Allow the user to read, modify and list directories
find "$1" -type d -exec setfacl -dm "${current_uid}:rwx"  {} \;  -exec setfacl -m "${current_uid}:rwx"  {} \;

# Allow the user to read and edit files and execute the ones
find "$1" -type f -print0 | 
    while IFS= read -r -d $'\0' fp; do 
        if [ -x "$fp" ]; then
            echo  "$fp"
            setfacl -m "${current_uid}:rwx"  "$fp"
        else 
            setfacl -m "${current_uid}:rw"  "$fp"
        fi
    done
#find  -exec sh -c "
