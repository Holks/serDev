# -*- coding: utf-8 -*-
#/usr/bin/python
import sys
import glob
import serial
import threading
import queue
import socket
import serial
from enum import Enum
import io

class ConnectionType(Enum):
    RS232 = 0
    SOCKET = 1

class SerialThread(threading.Thread):
    """Return the pathname of the KOS root directory."""
    def __init__(self, queue, ser=None):
        threading.Thread.__init__(self)
        self.ser = ser
        self.queue = queue
        self._stopevent = threading.Event()
        print("Thread")

    def find_serial():
        """
        Find all available COM ports connected to current system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(50)]
        elif sys.platform.startswith('linux') \
            or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try: # exception if not available
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def open_ser_connection(self, ser):
        try:
            print("Connecting " + str(ser['port']))
            self.conn = serial.Serial(ser['port'], ser['baudrate'],
                bytesize=8, parity='N', stopbits=1,timeout=0.1)
            print(self.conn)
            self.sio = io.TextIOWrapper(io.BufferedRWPair(self.conn, self.conn, 1),
                newline = '\r')
            self.sio._CHUNK_SIZE = 1
            return False
        except Exception as e:
            raise e from None

    def write(self, data):
        self.data =  data +"\r"

    def read(self):
        res = self.conn.readline()
        self.conn.flush()
        return res

    def run(self):
        while True:
            try:
                if self.conn.inWaiting():
                    text = self.sio.readlines()
                    print(text)
                    for line in text:
                        if line and line.find('\x03') == -1:
                            self.queue.put(line.strip())

                if self.data:
                    self.conn.write(self.data.encode())
                    self.data=None
                    #self.sio.flush()
            except:
                pass

class SocketThread(threading.Thread):
    def __init__(self, queue, sock=None):
        threading.Thread.__init__(self)
        self.data=None
        self.queue = queue
        self.conn = sock

    def write(self, data):
        try:
            if self.conn:
                print(data, self.conn)
                self.conn.send(data.encode())
        except Exception as e:
            raise e

    def read(self, bytes=1024):
        if self.conn:
            data = self.conn.recvfrom(bytes)
            return data[0]
        else:
            return None

    def run(self):
        while True:
            try:
                data_in = self.read_socket()
                if data_in:
                    print(data_in, float(data_in.decode()))
                    self.queue.put(float(data_in.decode()))
            except socket.timeout:
                pass
            except ValueError:
                self.queue.put("Out of range")
            except:
                pass
