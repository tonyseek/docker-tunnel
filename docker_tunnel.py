#!/usr/bin/env python

import os
import subprocess
import contextlib
import distutils.spawn

import click


__version__ = '0.1.0'
__all__ = ['local_forward_tunnel', 'main']


@contextlib.contextmanager
def local_forward_tunnel(local_addr, remote_addr, hostname):
    cmd = distutils.spawn.find_executable('ssh') or '/usr/bin/ssh'
    forward_string = '%s:%d:%s:%d' % (local_addr + remote_addr)
    proc = subprocess.Popen(
        [cmd, '-N', '-L', forward_string, hostname],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL)
    try:
        yield
    finally:
        proc.kill()
        proc.wait()


def shell(local_addr, hostname):
    cmd = os.environ.get('SHELL', '/bin/sh')
    env = dict(os.environ)
    env['DOCKER_HOST'] = 'tcp://%s:%d' % local_addr
    env['DOCKER_PROMPT_INFO'] = hostname
    proc = subprocess.Popen([cmd, '--login'], env=env)
    proc.wait()


@click.command()
@click.option('--local-host', default='127.0.0.1')
@click.option('--local-port', default=4243)
@click.option('--remote-host', default='127.0.0.1')
@click.option('--remote-port', default=2375)
@click.argument('hostname')
def main(local_host, local_port, remote_host, remote_port, hostname):
    local_addr = (local_host, local_port)
    remote_addr = (remote_host, remote_port)

    with local_forward_tunnel(local_addr, remote_addr, hostname=hostname):
        shell(local_addr, hostname)


if __name__ == '__main__':
    main()
