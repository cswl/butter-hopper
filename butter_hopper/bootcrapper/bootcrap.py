from pathlib import Path

import click

from butter_hopper.config_helper import read_all_config
from .flatduck import export_flatduck


class ConfigStore(object):
    def __init__(self):
        self.verbose = False

    def __repr__(self):
        return '<Repo %r>' % self.verbose


pass_config = click.make_pass_decorator(ConfigStore)

image_cache = Path.home().joinpath(".cache/bootcrapper/images")


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
    Bootstrap any distros with bootcrapper.
    """
    userconfig = read_all_config()
    ctx.obj = ConfigStore()
    ctx.obj.test = test
    ctx.obj.bootcrap = userconfig.main.bootcrapper


@cli.command()
@click.argument("distro")
@pass_config
def download(config, distro):
    """
    Download the specified distro rootfs image if available.
    """
    if config.test:
        print("Running in test mode.")
    if config.bootcrap.cache_dir:
        print("Using user specified cache.")
        image_cache = config.bootcrap.cache_dir
    print(config.bootcrap)
    return


@cli.command()
@click.argument("name")
@pass_config
def flat(config, name):
    """
    Download the specified distro rootfs image if available.
    """
    if config.test:
        print("Running in test mode.")
    if config.bootcrap.cache_dir:
        print("Using user specified cache.")
        image_cache = config.bootcrap.cache_dir
    #print(config.bootcrap)
    export_flatduck("busybox:latest")
    return
