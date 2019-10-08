## This script requires root

import docker
import click
import tempfile

client = docker.from_env()


def export_flatduck(image_name):
    tempfile.TemporaryDirectory(suffix="flatduck")
    image = client.images.pull('image_name')
    f = open('/tmp/busybox-latest.tar', 'wb')
    for chunk in image:
        f.write(chunk)
    f.close()

    click.echo(f"Exported ${image_name} as:")
