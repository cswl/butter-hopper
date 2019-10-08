#!/bin/bash

sudo debootstrap cosmic /mnt/
debootstrap cosmic /mnt
arch-chroot /mnt
