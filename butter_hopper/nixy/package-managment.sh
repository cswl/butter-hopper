

update_channels:
 nix-channel --update

Upgrade Packagee
nix-env -u --dry-run

Uprade system:
'nix-channel --update && nix-env -iA nixpkgs.nix '