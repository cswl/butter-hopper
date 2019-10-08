## butter-hopper

butter-hopper is a collection of tools to help making switching between multiple distros easier 
butter-hopper allows you to try out  multiple distros on a single large BTRFS partition using BTRFS subvolumes.

### Features:
- butter-hopper uses `systemd-nspawn` to `ch-boot` into your desired distro  
- And if you wanna take it for an actual spin on your hardware you can do that too   
- butter-hopper will extract boot entries in the OS and present them in GRUB/rEFInd menu.
- Installing and upgrading various common packages on many distros can be time consuming.    
     butter-hopper uses `nix` as package management/cache which can be used from any distro
- Support installing tools like IDE, VSCode which don't need to be packaged to `/common`
- PLANNED: Using qemu/KVM to boot GUI to another distro

### Pre:requesties
- Make sure all of distro use systemd and support btrfs which should be any recent distro
- For the boot to hardware you want to make sure you have a recent version of GRUB2 installed with  
support for btrfs.

### butter hopper tools
- `btrhop` : The main command line interface to btrhop which allows managing snapshots, running, upgrading distros
- `bootcrap`  : Command line tools to bootstrap a distro from rootfs or docker images.
- `mntem` : A tool to help manage multiple mount points of BTRFS subvolumes/ shared storage.
- `nixy` : Helper script to install `nix` and setup packages on common `/nix/store`

### Sharing:
While using a default user of `1000` and allowing any user to change stuffs in `/home` works.  
`butter-hopper` recommends using differnt user ids of your primary user and supports in the config.   
To take a sample config of `butter-hopper.conf` look at my dotfile in your preferred Git hosting.  
[![Github](https://i.imgur.com/7UwDPus.png)](https://github.com/cswl/dotfiles/tree/master/config/butter-hopper)
[![Gitlab](https://i.imgur.com/G6QcEk4.jpg)](https://gitlab.com/cswl/dotfiles/tree/master/config/butter-hopper)
[![Bitbucket](https://i.imgur.com/TKS3S7F.png)](hhttps://bitbucket.org/cswl/dotfiles/src/master/config/butter-hopper/)

### Tips:
Change your default subvol to "/staging" so you dont accidentally mount the real root   
To do that simply run  `btrhop populate-distros --staging`


### Working
This is the layout pulled directly from my current install.
butter-hopper installs distros to `/distros` in your btrfs partition  

```
distros
       ├── arch
       │   ├── @
       │   └── home
       ├── debian-buster
       │   ├── @
       │   └── home
       ├── fedora
       │   ├── @
       │   └── home
       ├── tumbleweed
       │   ├── @
       │   └── home
       ├── ubuntu-latest
       │   ├── @
       │   └── home
```


### License
Copyright (c) 2019 Cswl Coldwind <cswl1337@gmail.com>
Licensed under the MIT License. See LICENSE.txt