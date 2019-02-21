﻿# -*- coding: utf-8 -*-
#/usr/bin/python3

from modules.handler import send_data_klm
from devices import ptb330
from config import logger
import sys

if __name__ == "__main__":
    sensors = []
    pressure_1 = ptb330.VaisalaPTB330(serial_conn={'port':'/dev/ttyUSB0','baudrate':19200,
        'bits':8, 'parity':'N', 'stop_bits': 2})
    """try:
        for sensor in sensors:
            send_data_klm(sensor.get_json_data())
    except Exception as e:
        logger.error('EXCEPTION occured', exc_info=True)
    """
    try:
        while True:
            pressure_1.write_device("TEST")
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
