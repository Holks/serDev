import msvcrt
import time
import threading
import queue
import sys
import socket
from modules.threads import SocketThread
import os
import json

class SerialToEthernetDevice():
    ip = None
    port = None
    descriptor = None
    device = None

    def __init__(self, ip, port, descriptor=None):
        self.ip = ip
        self.port = port
        self.descriptor = descriptor

    def __repr__(self):
        return json.dumps(self.get_json(), sort_keys=True, indent=4)
    def get_json(self):
        return {'ip':self.ip, 'port':self.port, \
            'descriptor':self.descriptor}
    def connect(self, queue):
        self.device = SerialToEthernet()
        self.device.connect(self.get_json())
        if self.device.socket:
            self.thread = SocketThread(queue, sock=self.device.socket)
            self.thread.daemon = True
            #self.thread.conn = self.device.socket
        else:
            self.device = None
    def start_thread(self):
        print("Start thread")
        self.thread.start()
    def find_devices(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        print(cwd)
        filename = os.path.join(cwd, device_list_filename)
        with open(filename,'r') as f:
            count = 0
            for line in f:
                dev = line.strip().split(';')
                dev = SerialToEthernetDevice(dev[0],dev[1],descriptor=dev[2])
                yield (count, dev)
                count += 1
    def get_connection(self):
        return json.dumps(self.get_json())
    def device_close(self):
        self.device.device_close()
        self.thread.join(timeout=0.1)
        self.ip = None
        self.port = None
        self.descriptor = None
        self.device = None

class SerialToEthernet():
    def __init__(self):
        self.socket = None

    def connect(self, dev_socket):
        s = None
        for res in socket.getaddrinfo(dev_socket['ip'], dev_socket['port'],
                socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except OSError as msg:
                s = None
                continue
            try:
                s.settimeout(5)
                s.connect(sa)
            except OSError as msg:
                s.close()
                s = None
                continue
            self.socket = s
            break
        return s

    def write(self, data):
        self.socket.send(data.encode())

    def device_close(self, socket=None):
        if socket:
            socket.close()
        else:
            self.socket.close()
