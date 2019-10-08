#!/bin/bash

SYSTEMD_USER_CONFIGS="/etc/systemd/system"

pushd . > /dev/null
SCRIPT_PATH="${BASH_SOURCE[0]}";
if ([ -h "${SCRIPT_PATH}" ]) then
  while([ -h "${SCRIPT_PATH}" ]) do cd `dirname "$SCRIPT_PATH"`; SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
fi
cd `dirname ${SCRIPT_PATH}` > /dev/null
SCRIPT_PATH=`pwd`;
popd  > /dev/null

echo "Removing previous installated services"
sudo rm "${SYSTEMD_USER_CONFIGS}/nix-daemon.service"
sudo rm "${SYSTEMD_USER_CONFIGS}/nix-daemon.socket"

sudo cp "$SCRIPT_PATH/nix-daemon.service" "${SYSTEMD_USER_CONFIGS}/nix-daemon.service"
sudo cp "$SCRIPT_PATH/nix-daemon.socket" "${SYSTEMD_USER_CONFIGS}/nix-daemon.socket"

star() {
    sudo systemctl start nix-daemon.socket
    sudo systemctl start nix-daemon.service
}

enable {
    sudo systemctl enable nix-daemon.socket
    sudo systemctl enable nix-daemon.service
}