import logging
import subprocess

import shlex
import click
from shell import shell

# create sudo  logger
logger = logging.getLogger('sudo_call_shell')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()

formatter = logging.Formatter('sudo %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def sudo_call_shell(shell_cmd):
    logger.debug(shell_cmd)
    shell(f'sudo {shell_cmd}')


def sudo_call(shell_cmd):
    logger.debug(shell_cmd)
    sudo_cmd = ['sudo'] + shlex.split(shell_cmd)
    subprocess.call(sudo_cmd)


def unpriv_call(shell_cmd):
    subprocess.call(shlex.split(shell_cmd))
