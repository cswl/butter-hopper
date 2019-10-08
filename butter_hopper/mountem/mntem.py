import click

from munch import Munch
from butter_hopper.config_helper import read_all_config
from butter_hopper.utils_mount import MountGeneric


@click.command()
@click.argument("name")
def cli(name):
    """
    Utility to mount devices and btrfs subvolumes.
    """

    userconfig = read_all_config()
    mounts = userconfig.mounts
    # Search for the moutn name in the config file
    for entry, val in mounts.items():
        #print(entry, val)
        if entry == name:
            mount = MountGeneric(entry, Munch(val))
            mount.perform()
    return
