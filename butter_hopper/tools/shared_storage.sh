#!/bin/bash


add_to_group() {
## Allows sharing of files between different distro users
groupadd -g 99968 shared_users
## Shared storage permissions:
usermod -aG shared_users "$1"
}

## User ids are from 10,000 to 19,999
## Shared group id is 99,968 
## Ids greater than 100,000 are used for unpriveleged containers

# Fix permissions
if [ "$1" == "fix" ]; then 

fi;