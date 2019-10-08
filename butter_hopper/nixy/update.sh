#!/bin/bash 

sudo -i sh -c 'nix-channel --update && nix-env -iA nixpkgs.nix '
