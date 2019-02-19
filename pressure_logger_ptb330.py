# -*- coding: utf-8 -*-
#/usr/bin/python3
import time, urllib.request
import unittest
import threading
import serial_thread.seerial as ser_thread
from time import sleep
import queue
from serial.serialutil import SerialException, SerialTimeoutException
import serial
from enum import Enum
from datetime import datetime
import json
import sys
from config import Config

class MeasurementQuantity(Enum):
    temperature = 0
    humidity = 1
    pressure = 2
class Sensor():
    quantity = None
    reading = None
    timestamp = None
    unit = None
    id = None
    connection = None

    def __repr__(self):
        print( {
            "rdg":self.reading,
            "qty":self.quantity,
            "timestamp":self.timestamp,
            "unit":self.unit,
            "id":self.id,
            "conn":self.connection
            })

class VaisalaPTB330(Config):
    repeater = True
    sensors = []
    sensing_mode = False
    device_SN = None
    def __init__(self, port=None, baudrate=19200, timeout=3, \
        bytesize=8, parity='E', stopbits=1):
        self.queue = queue.Queue()
        self.thread = ser_thread.SerialThread(self.queue)
        self.thread.daemon = True

        print(port,baudrate)
        if not port:
            self.port = self.get_port()
        if self.port and baudrate:
            ser = {'port': self.port,'baudrate':baudrate}
            self.open_connection(ser)
            self.process_serial()
    def open_connection(self, ser):
        try:
            if not self.thread.ava_seerial(ser):
                self.thread.start() # käivitab seeriali lõime
        except SerialException:
            print("Serial error")
        except Exception as e:
            print("ERROR\n{0}".format(e))

    def write(self, data):
        #print("data out '{}'".format(data))
        self.thread.write_serial(data)

    def get_port(self):
        available_ports = ser_thread.find_serial()
        print(available_ports)
        try:
            for port in available_ports:
                print("Trying connection on {}".format(port))
                if not int(port.split('COM')[1]) in [6]:
                    s = serial.Serial(port)
                    s.baudrate=19200
                    s.timeout=1
                    print("Serial out: {}".format(device_firmware.encode()))
                    sleep(.1)
                    s.flushInput()
                    s.flushOutput()
                    s.write((device_firmware+'\r').encode())
                    print("Trying reading")
                    sleep(.1)
                    resp = s.read(1000)
                    print(resp)
                    if "PTB330".encode() in resp:
                        s.close()
                        return port
                    s.close()
        except serial.SerialException as e:
            print(e)
        except Exception as e:
            print(e)
    def apply_sensor(self, data):
        try:
            connected_sensor = Sensor()
            connected_sensor.unit = 'hPa'
            connected_sensor.id = data['id']
            connected_sensor.connection = data['device']
            connected_sensor.quantity =  MeasurementUnit(2).name
            #connected_sensor.__repr__()
            self.sensors.append(connected_sensor)
        except Exception as e:
            print("{}".format(e))

    def get_serial_number(self):
        return self.write(serial_number)

    def get_sensor_data(self, data):
       # device_list = data_output_format.strip('\"').split(';')
       # print(device_list)
       # print(data)
        for i, value in enumerate(data.split(";")[2:]):
         #   print(value)
            try:
                self.sensors[i].reading = value
                self.sensors[i].timestamp = 0
                send_data(self.sensors[i])
            except:
                pass

    def process_serial(self):
        while self.queue.qsize():
            try:
                data_in = self.queue.get().strip()
                if "PTB330 / 1.14" in data_in:
                    pass
                    #self.apply_sensor(data_in.lower())
                elif 'Serial number' in data_in:
                    self.device_SN = data_in.strip().split(":")[1].strip()
                   # print("device serial no : {}".format(self.device_SN))
                    device = {'id': self.device_SN, 'device': 'P_AVG'}
                    self.apply_sensor(device)
                elif data_in.find('serial') > 0:
                    module_id = data_in.strip().split(":")
                  #  print("module id : {}".format(module_id))
                    module_sensor_no = module_id[0].split(" ")[1]
                 #   print("module sn : {}".format(module_sensor_no))
                    module = {'id': module_id[1].strip(), 'device': 'P'+str(module_sensor_no)}
                    self.apply_sensor(module)
                elif self.sensing_mode:
                    self.get_sensor_data(data_in)
                else:
                    print(data_in)
            except queue.Empty:
                pass
        if self.repeater:
            threading.Timer(0.01, self.process_serial).start()
    def get_sensor_readings(self):
        self.write(reading)
    def get_sensor_types(self):
        self.write(sensor_descriptions)
        sleep(1)
    def apply_data_format(self):
        self.write(data_output_format)
        sleep(5)
        self.write(default_unit)
        sleep(5)


def send_data(sensor):
    t1 = aadress + "%20" + "VAISALA_PTB330_" + str(sensor.id) + "%20" + str(sensor.reading.replace(',','.')).strip(' ') + "%20" + str(sensor.quantity) + aadress2# + str(sensor.timestamp)
    result = urllib.request.urlopen(t1)
    print(t1+str(result.read()))


if __name__ == "__main__":
    # open connection
    pressure_sensor = VaisalaPTB330()
    # get device firmware info
    pressure_sensor.write(device_firmware)
    sleep(1)
    pressure_sensor.get_serial_number()
    sleep(10)
    # delay to allow the sensor to respond
   # print("No of sensors connected: {}".format(len(pressure_sensor.sensors)))
    if len(pressure_sensor.sensors)  > 0 :
        pressure_sensor.apply_data_format()
        for i in range(1):
            pressure_sensor.get_sensor_readings()
            pressure_sensor.sensing_mode = True
            sleep(5)

    sleep(3)
    pressure_sensor.repeater = False
