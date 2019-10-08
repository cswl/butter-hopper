from munch import Munch
from pathlib import Path

MOUNT_HEADERS = Munch({
    "BTRFSROOT_TARGET": 'broot',
    "UUID": "uuid",
    "PARTUUID": "puuid",
    "TYPE": "type",
    "AUTO": "auto",
    "SUBVOL": "subvol",
    "TARGET": "mountpoint",
    "OPTIONS": "options",
    "UDISKS_TARGET": "udisks2"
})

BASE_PATHS = Munch({})
BASE_PATHS.run = Path('/run/mount')
BASE_PATHS.base = BASE_PATHS.run.joinpath('butter_hop')
BASE_PATHS.dlinks = BASE_PATHS.base.joinpath("distros")
BASE_PATHS.root = BASE_PATHS.run.joinpath("butter_realroot")
BASE_PATHS.distros = BASE_PATHS.root.joinpath("distros")
