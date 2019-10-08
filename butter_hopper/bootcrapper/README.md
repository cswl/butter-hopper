## bootcrapper and flat duck
### bootstrap any distro

Flatten docker images for use in another containerzation systems mainly `systemd-nspawn`

### Why?
Docker images are **layered** and supposed to be **immutable**.  
Which is nice for software development but not so if you wanna use them as an `guest os` without  
the overhead of actual Virtualization.

Flat duck flattens base docker images to a `rootfs` which is then copied to a `btrfs` subvolume.  
 
Now you have a `rootfs`  in a btrfs subvolume which you can boot via.. `systemd-nspawn`   
take snapshots, install packages and have a  fully functional secondary OS  
containerzied
