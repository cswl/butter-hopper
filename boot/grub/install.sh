#!/bin/sh

GRUB_PREFIX="/boot/grub"

install -m0755 50-custom_entry /etc/grub.d/50-custom_entry
install -m0644 extract.cfg "$GRUB_PREFIX/extract.cfg"

grub-mkconfig -o "$GRUB_PREFIX/grub.cfg"