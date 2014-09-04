#!/usr/bin/env python

import os
import threading
import subprocess
from socketserver import ThreadingTCPServer, BaseRequestHandler
from selectors import DefaultSelector, EVENT_READ

import click
import paramiko


class LocalForwardServer(ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class ProxyHandler(BaseRequestHandler):

    chunk_size = 1024

    def handle(self):
        self.ssh_channel = self.ssh_transport.open_channel(
            'direct-tcpip', self.chain_addr, self.request.getpeername())

        selector = DefaultSelector()
        selector.register(self.request, EVENT_READ, 'request')
        selector.register(self.ssh_channel, EVENT_READ, 'channel')

        while True:
            for key, mask in selector.select():
                if key.data == 'request':
                    data = self.request.recv(self.chunk_size)
                    if not data:
                        break
                    self.ssh_channel.send(data)
                if key.data == 'channel':
                    data = self.ssh_channel.recv(self.chunk_size)
                    if not data:
                        break
                    self.request.send(data)

        self.ssh_channel.close()
        self.request.close()


def local_forward_tunnel(local_addr, remote_addr, **ssh_kwargs):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh_client.connect(**ssh_kwargs)

    class Handler(ProxyHandler):
        chain_addr = remote_addr
        ssh_transport = ssh_client.get_transport()
        ssh_keep_connection = ssh_client  # keep the reference of client

    server = LocalForwardServer(local_addr, Handler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    return server_thread


def shell(local_addr, hostname):
    cmd = os.environ.get('SHELL', '/bin/sh')
    env = {
        'DOCKER_HOST': 'tcp://%s:%d' % local_addr,
        'DOCKER_PROMPT_INFO': hostname,
    }
    proc = subprocess.Popen([cmd], env=env)
    exit(proc.wait())


@click.command()
@click.option('--local-host', default='127.0.0.1')
@click.option('--local-port', default=4243)
@click.option('--remote-host', default='127.0.0.1')
@click.option('--remote-port', default=2375)
@click.argument('hostname')
def main(local_host, local_port, remote_host, remote_port, hostname):
    local_addr = (local_host, local_port)
    remote_addr = (remote_host, remote_port)

    tunnel = local_forward_tunnel(
        local_addr, remote_addr, hostname=hostname)
    tunnel.start()

    shell(local_addr, hostname)


if __name__ == '__main__':
    main()
