#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import logging
import socket
import threading
import paramiko
import sys

from .utils import ssh_key_gen
from .interface import SSHInterface
from .interactive import InteractiveServer
from .models import Client, Request

logger = logging.getLogger(__file__)
BACKLOG = 5


class SSHServer:

    def __init__(self, app):
        self.app = app
        self.stop_evt = threading.Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_key_path = os.path.join(self.app.root_path, 'keys', 'host_rsa_key')

    @property
    def host_key(self):
        if not os.path.isfile(self.host_key_path):
            self.gen_host_key()
        return paramiko.RSAKey(filename=self.host_key_path)

    def gen_host_key(self):
        ssh_key, _ = ssh_key_gen()
        with open(self.host_key_path, 'w') as f:
            f.write(ssh_key)

    def run(self):
        host = self.app.config["BIND_HOST"]
        port = self.app.config["SSHD_PORT"]
        print('Starting ssh server at {}:{}'.format(host, port))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(BACKLOG)
        while not self.stop_evt.is_set():
            try:
                sock, addr = self.sock.accept()
                logger.info("Get ssh request from {}: {}".format(addr[0], addr[1]))
                thread = threading.Thread(target=self.handle, args=(sock, addr))
                thread.daemon = True
                thread.start()
            except Exception as e:
                logger.error("Start SSH server error: {}".format(e))

    def handle(self, sock, addr):
        transport = paramiko.Transport(sock, gss_kex=False)
        try:
            transport.load_server_moduli()
        except IOError:
            logger.warning("Failed load moduli -- gex will be unsupported")

        transport.add_server_key(self.host_key)
        request = Request(addr)
        server = SSHInterface(self.app, request)
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            logger.warning("SSH negotiation failed")
            return
        except EOFError:
            logger.warning("Handle EOF Error")
            return

        chan = transport.accept(10)
        if chan is None:
            logger.warning("No ssh channel get")
            return

        server.event.wait(5)
        if not server.event.is_set():
            logger.warning("Client not request a valid request, exiting")
            return

        client = Client(chan, request)
        self.app.add_client(client)
        self.dispatch(client)

    def dispatch(self, client):
        request_type = client.request.type
        if request_type == 'pty':
            logger.info("Request type `pty`, dispatch to interactive mode")
            InteractiveServer(self.app, client).interact()
        elif request_type == 'exec':
            pass
        elif request_type == 'subsystem':
            pass
        else:
            client.send("Not support request type: %s" % request_type)

    def shutdown(self):
        self.stop_evt.set()
