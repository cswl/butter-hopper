
from pathlib import Path

import ruamel.yaml
import configparser

from munch import Munch, munchify

yaml = ruamel.yaml.YAML()

## Configuration locations.
config_basedir = Path.home().joinpath(".config/butter-hopper")
config_distros = config_basedir.joinpath("distros.yaml")
config_main = config_basedir.joinpath("config.yaml")
config_mounts = config_basedir.joinpath("mount.conf")

#   -


def read_all_config():
    mount_config = configparser.ConfigParser(allow_no_value=True)

    with open(config_distros) as data_file:
        user_distros_conf = yaml.load(data_file)

    with open(config_main) as data_file:
        user_main_conf = yaml.load(data_file)

    with open(config_mounts) as data_file:
        mount_config.readfp(data_file)
        user_mounts_conf = {
            s: dict(mount_config.items(s))
            for s in mount_config.sections()
        }

    config_maps = Munch({
        "distros": munchify(user_distros_conf),
        "mounts": munchify(user_mounts_conf),
        "main": munchify(user_main_conf)
    })
    #print (config_maps)
    return config_maps
