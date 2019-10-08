import subprocess
from pathlib import Path

from .headers import MOUNT_HEADERS, BASE_PATHS

from .executor import NspawnManager
from .utils_exec import sudo_call_shell, sudo_call, unpriv_call

### Common methods


def _uuid_to_dev(uuid):
    return f'/dev/disk/by-uuid/{uuid}'


def _puuid_to_dev(puuid):
    return f'/dev/disk/by-partuuid/{puuid}'


def mount_distro_helper(btrfs_uuid, distro):
    mount = MountDistros(btrfs_uuid)
    mount.set_distro(distro)
    mount.bind()


class MountDistros(object):
    def __init__(self, dev_uuid):
        """ Need the device UUID and distro_name only
        """
        self.dev_uuid = dev_uuid
        self.dev_block_path = _uuid_to_dev(self.dev_uuid)

    def set_distro(self, distro_data):
        self.distro_data = distro_data
        self.distro_name = distro_data.get('name')

    def _get_distro_mount_paths(self):
        """ Returns mount points for root subvolmes of distros
        /distros/<distro_name>/@
        /<distros>/<distro_name>
        """
        distro_name = self.distro_name
        return (BASE_PATHS.root.joinpath(f'/distros/{distro_name}/@'),
                BASE_PATHS.dlinks.joinpath(distro_name))

    def _get_distro_home_paths(self):
        """ Returns mount points for home subvolmes of distros
        /distros/<distro_name>/home
        /<distros>/<distro_name>/home
        """
        distro_name = self.distro_name
        return (BASE_PATHS.distros.joinpath(f'/distros/{distro_name}/home'),
                BASE_PATHS.dlinks.joinpath(f'{distro_name}/home'))

    def _distro_home(self):
        distro_name = self.distro_name
        home_subvol_option, home_subvol_mount = self._get_distro_home_paths()
        if not home_subvol_mount.is_mount():
            sudo_call_shell(
                f'mount -o "subvol={home_subvol_option}" {self.dev_block_path} {home_subvol_mount}'
            )
        print(f'Mounted /home for {distro_name}')

    def _distro_root(self):
        distro_name = self.distro_name
        root_subvol_option, root_subvol_mount = self._get_distro_mount_paths()
        if not root_subvol_mount.is_mount():
            sudo_call_shell(
                f'mount -o "subvol={root_subvol_option}" {self.dev_block_path} {root_subvol_mount}'
            )
        print(f'Mounted @ for {distro_name}')

    def ensure_distro_paths(self):
        distro_name = self.distro_name
        butter_paths = [
            str(BASE_PATHS.run),
            str(BASE_PATHS.base),
            str(BASE_PATHS.dlinks)
        ]
        distro_links_path = BASE_PATHS.dlinks.joinpath(distro_name)

        # Try to create the distro active paths.
        sudo_call_shell(f'mkdir -p {butter_paths[2]}')

        # Check if we already have created the active distro dir
        if not distro_links_path.is_mount():
            sudo_call_shell(f'mkdir {distro_links_path}')

        return distro_links_path

    def bind(self):
        dpath = self.ensure_distro_paths()
        if not dpath.is_mount():
            # Create subvol mount for active distros
            self._distro_root()
            self._distro_home()


class MountGeneric(object):
    """ Utility class to mount disks, udisks2,BTRFS subvolumes
    """
    def __init__(self, mntname, mntcfg):
        """Selects appropriate UUID or Part UUID
        """
        self.name = mntname
        self.cfg = mntcfg
        #print(mntname, mntcfg)
        if "uuid" in mntcfg:
            self.dev_blk = _uuid_to_dev(mntcfg.uuid)
        elif "puuid" in mntcfg:
            self.dev_blk = _puuid_to_dev(mntcfg.puuid)
        else:
            raise AttributeError('No UUIDs/ Part UUIDs configured')

        self.target = self.cfg.get(MOUNT_HEADERS.TARGET)
        if MOUNT_HEADERS.OPTIONS in mntcfg:
            self.opts = self.cfg.get(MOUNT_HEADERS.OPTIONS)
        else:
            self.opts = ''
        if MOUNT_HEADERS.SUBVOL in mntcfg:
            self.subvol = mntcfg.get(MOUNT_HEADERS.SUBVOL)
            self.opts += f'subvol={self.subvol}'

    def realbtrfsroot(self):
        """ Mounts the real btrfs root to /run/mount/butter_realroot
        """
        if not BASE_PATHS.root.is_mount():
            root_mount_path = str(BASE_PATHS.root)
            sudo_call_shell(f'mkdir -p {root_mount_path}')
            sudo_call_shell(
                f'mount -o subvolid=5 {self.dev_blk} {root_mount_path}')

    def btrfs_subvol(self, subvol_path, mount_point):
        sudo_call_shell(
            f'mount -o subvol={subvol_path} {self.dev_blk} {mount_point} ')

    def raw(self):

        print("Mounting with sudo.")
        #print(opts)
        sudo_call(f'mount -o "{self.opts}" {self.dev_blk}  {self.target}')

    def udisks(self):
        print("Mounting with Udisks.")
        unpriv_call(f'udisksctl mount -b {self.dev_blk}')

    def unmount(self):
        print(f'Unmounting... {mount_path}')
        sudo_call_shell(f'umount ${mount_path}')

    def perform(self):
        if self.name == MOUNT_HEADERS.BTRFSROOT_TARGET:
            self.realbtrfsroot()
        elif self.target == MOUNT_HEADERS.UDISKS_TARGET:
            self.udisks()
        else:
            self.raw()
