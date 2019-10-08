### Nixy xoxo

A portable-ish way to use Linux apps on multiple distros.

## Why did I choose Nix packages over others ?
- **Docker** : 
    - Running GUI apps is hacky.. And you need to mess with bind mounts for CLI
    - An update in any layer requires rebuilt of all layers.. since "images" are supposed to be immutable
    - Is really used for micro-services.. people use it for everything
- **Snap** :
    - Uses squashfs.. and shittons of bind mounts.. 
    - Messes with systemd stuffs, sandboxing is good but is it really necessary
    - Nice idea overall.. but has shit implementation
- **AppImage**:
    - Uses FUSE.. just fuck FUSE.
    - One app = one file.. sounds good doesn't work

## Why use Nix?
- Functional.
- Can be installed in multi-user mode.. where each user has seperate profile.
- Everything is in `/nix/store` which can be made a seperate BTRFS subvolume.
- Each user can have different sets of packages and some can be made system-wide.


### Using with butter-hop

Update channel.. ala "sudo apt update"
 nix-channel --update

Upgrading Packagee
nix-env -Au 