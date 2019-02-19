# -*- coding: utf-8 -*-
#/usr/bin/python3

import serial
import json
import sys
from modules.threads import SerialThread

class TesaSerialDevice(serial.Serial):
    def __repr__(self):
        return json.dumps(self.get_json(), sort_keys=True, indent=4)
    def get_json(self):
        return {'COM':self.port, 'baudrate':self.baudrate, \
            'protocol':str(self.bytesize)+str(self.parity)+str(self.stopbits)}
    def connect(self, queue):
        self.device = self.test_serial()
        self.thread = SerialThread(queue,ser=self.device)
        self.thread.daemon = True
    def find_devices():
        """Function for searching available serial ports"""
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
            try:
                s = TesaSerialDevice(port)
                s.close()
                result.append(s)
            except (OSError, serial.SerialException):
                pass
        return result
    def test_serial(self):
        tt90 = TT20(port=self.port, baudrate=4800)
        tt90_in = tt90.getValue()
        if tt90_in != 'None':
            print("Using TT90\n")
            return tt90
        else:
            print("Using TESA MODUL\n")
            del(tt90)
            tt20 = TT20(port=self.port, baudrate=1200)
            return tt20
        pass
    def start_thread(self):
        self.thread.start()
    def get_connection(self):
        return json.dumps(self.get_json())
    def device_close(self):
        # TODO: close port
        print("Closing port {}".format(json.dumps(self.get_json())))
        self.thread.join(timeout=0.1)
        self.device._conn.close()
        self.device = None

class TT20():
    def __init__(self, port, baudrate=4800):
        try:
            self._conn = serial.Serial(port=port, baudrate=baudrate,
                                  bytesize=7, parity='E', stopbits=2,
                                  timeout=0.5, xonxoff=0, rtscts=0)
        except  serial.SerialException as ex:
            print ("Port {0} is unavailable:".format(port, ex))
            self._conn.flush()
            self._conn.send_break()
            return
    def write(self, data):
        sn = (('%s\r'%data).encode('utf-8'))
        self._conn.write(sn)
    def read(self):
        self._conn.setRTS(0)
        res = self._conn.readline()
        self._conn.flush()
        if len(res) > 5 :
            print(res)
            return clean(res)
    def getValue(self):
        self.write("?")
        res = self.read()
        return str(res)
    def waitValue(self):
        self._conn.setRTS(0)
        res = self._conn.readline()
        self._conn.flush()
        return str(clean(res))
