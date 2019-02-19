"""
Pressure sensor data aquisition
"""
import time
import queue
import sys
from modules.ptb330 import PTB330
from modules.usrIOT import SerialToEthernetDevice, SerialToEthernet
from enum import Enum
import os
import json


# change to get more measurement per one aquisition
measurement_qty = 1

def help_print():
    import ptb330
    print("Measurements per aquisition: {}".format(measurement_qty))
    print("Pressure module ip: {0}".format(pressure_module['ip']))
    print("Pressure module port: {0}".format(pressure_module['port']))
    print(ptb330.__doc__)

def send_data(sensor):
    t1 = aadress + "%20" + "VAISALA_PTB330_" + str(sensor.id) + "%20" + str(sensor.reading.replace(',','.')).strip(' ') + "%20" + str(sensor.quantity) + aadress2# + str(sensor.timestamp)
    result = urllib.request.urlopen(t1)
    print(t1+str(result.read()))

def data_query():
    pass

if __name__ == "__main__":
    """
    Get data from pressure module VAISALA PTB330
    """
    for i in range(measurement_qty):
        # get no of measurement results
        data_query()
