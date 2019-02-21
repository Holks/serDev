﻿# -*- coding: utf-8 -*-
#/usr/bin/python3
import os
import logging
from logging.handlers import RotatingFileHandler
import json

class Config:
    serial_conn = os.environ.get("PRESSURE_MODULE_SERIAL_CONN")
    if serial_conn:
        serial_conn = json.loads(serial_conn)
    else:
        serial_conn = {'baudrate':19200, 'bits':8, 'parity':'N', 'stop_bits': 2}
    socket = os.environ.get("PRESSURE_MODULE")
    if socket:
        socket = json.loads(socket)
    else:
        socket = {'ip':'10.1.1.73', 'port':24}
    measurement_qty = 1

DATABASE_CONFIG = {
        'base_uri' : "http://10.1.1.254/klm/?t=mootmine&tulem=0",
        'dev_id' : "",
        'dev_rdg' : "",
        'dev_qty' : "",
        'rdg_timestamp' : "&k_stamp=0"
}
LOGFILE = os.environ.get("DATA_LOGGER_LOG") or 'logs/data_logger.log'

logger = logging.getLogger(__name__)
# logger level INFO basically anything
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]')

file_handler = RotatingFileHandler(LOGFILE, mode='a+', maxBytes=10240,
    backupCount=10)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.info('Starting data acquisition')
