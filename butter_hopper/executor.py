import os

from pathlib import Path

import shlex
import click
from shell import shell

from .headers import BASE_PATHS
from .utils_exec import sudo_call_shell, sudo_call

#from .utils_mount import MountBtrfs


class NspawnManager(object):
    """ Utility class to manage booting of distros
    """
    def __init__(self, distro_data):
        """ Reads distro data and assigns stuffs.
        """
        self.distro_data = distro_data
        self.distro_name = self.distro_data.get('name')
        self.distro_root_path = BASE_PATHS.dlinks.joinpath(self.distro_name)

    def boot(self):
        """Boot into the selected distro.
        
        """
        click.echo(f"Attempting to boot {self.distro_name}")
        #print(self.distro_path)
        sudo_call(
            f'systemd-nspawn -M {self.distro_name} -bD {self.distro_root_path}'
        )

    def shell(self):
        print(self.distro_name)
        sudo_call(
            f'systemd-nspawn -M {self.distro_name} -D {self.distro_root_path}')
        pass

    def unsafe_chroot(self):
        chroot_path = str(ensure_paths(self.distro_name, dev_uuid))
        mount_as_subvol(distro, dev_uuid)
        #sudo_call_shell(f'arch-chroot {chroot_path}')
        pass
