import os
import sys

from pathlib import Path
from munch import Munch
import click

from .config_helper import read_all_config
from .headers import MOUNT_HEADERS
from .utils_base import extract_distros
from .utils_mount import MountDistros, MountGeneric, mount_distro_helper
from .executor import NspawnManager


class ConfigStore(object):
    def __init__(self, userconfig):
        self.userconfig = userconfig
        self.verbose = False

    def __repr__(self):
        return '<Repo %r>' % self.userconfig


pass_config = click.make_pass_decorator(ConfigStore)


@click.group()
@click.option("--test",
              is_flag=True,
              help="Only test commands but dont run them.")
@click.option("--verbose",
              "-v",
              is_flag=True,
              help="Only test commands but dont run them.")
@click.pass_context
def cli(ctx, test, verbose):
    """
    Command line interface of butter hopper.
    """
    userconfig = read_all_config()
    btrfs_device = userconfig.mounts[MOUNT_HEADERS.BTRFSROOT_TARGET]
    btrfs_dev_uuid = btrfs_device.get(MOUNT_HEADERS.UUID)
    # Create a ConfigStore object and remember it as as the context object.  From
    # this point onwards other commands can refer to it by using the
    # @pass_repo decorator.
    ctx.obj = ConfigStore(userconfig)
    ctx.obj.test = test
    ctx.obj.verbose = verbose
    ctx.obj.distro_maps = userconfig.distros
    ctx.obj.btrfs_uuid = btrfs_dev_uuid


def validate_distro(distro_maps, name):
    try:
        sel_distro = extract_distros(distro_maps)[name]
        sel_distro['name'] = name
        return sel_distro
    except KeyError:
        raise click.UsageError(f'No such distro found. {name}')


@cli.command()
@pass_config
def info(config):
    """
    Display information of current config.
    """
    print(f"BTRFS device at UUID : {config.btrfs_uuid}")
    print("Following distros are configured", end="\n\n")
    for distro, val in config.distro_maps.items():
        print(f'{distro} :  {val}')
    return


@cli.command()
@click.argument("distro")
@pass_config
def bind(config, distro):
    """
    Mount the selected distro.
    """
    distro_data = validate_distro(config.distro_maps, distro)
    #print(distro_data, config.btrfs_uuid)
    mount_distro_helper(config.btrfs_uuid, distro_data)


@cli.command()
@click.argument("distro")
@pass_config
def boot(config, distro):
    """
    Boot into the selected distro using `systemd-nspawn`
    """
    distro_data = validate_distro(config.distro_maps, distro)
    # Ensure the distro has been mounted.
    mount_distro_helper(config.btrfs_uuid, distro_data)
    nspawn = NspawnManager(distro_data)
    nspawn.boot()


@cli.command()
@click.argument("distro")
@pass_config
def shell(config, distro):
    """
    Drop into a root shell of the distro.
    """
    distro_data = validate_distro(config.distro_maps, distro)
    # Ensure the distro has been mounted.
    mount_distro_helper(config.btrfs_uuid, distro_data)
    nspawn = NspawnManager(distro_data)
    nspawn.shell()


@cli.command()
@click.argument("distro")
def unsafechroot():
    """
    Use the un-safe chroot uses `arch-install scripts`
    """
    arch_chroot_into(distro_name, btrfs_dev_uuid)
