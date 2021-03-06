﻿# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler
import json
from dotenv import load_dotenv

"""Project root folder"""
basedir = os.path.abspath(os.path.dirname(__file__))
""" Load project environment variables from project ROOT dir.

NB! Do not include .env file in project source control
"""
load_dotenv(os.path.join(basedir, '.env'))

"""Project documentation directory.

Documentation files powered by sphinx module.
"""
docs_dir=os.path.join(basedir,'docs/_build/html')
print(docs_dir)

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
        socket = {'ip':'192.168.0.29', 'port':24}
    measurement_qty = 1
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    SECRET_KEY = os.environ.get('SERDEV_SECRET_KEY')
    print(SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_DEST_URL = os.environ.get('DEFAULT_DEST_URL') or \
        "http://10.1.1.254/klm"
    DEFAULT_DEST_DATA_FORMAT = os.environ.get('DEFAULT_DEST_DATA_FORMAT') or \
        "?t=mootmine&tulem=0 %s %s &s &k_stamp=0"

DATABASE_CONFIG = {
        'base_uri' : "http://10.1.1.254/klm/?t=mootmine&tulem=0",
        'dev_id' : "",
        'dev_rdg' : "",
        'dev_qty' : "",
        'rdg_timestamp' : "&k_stamp=0"
}
LOGFILE = os.environ.get("DATA_LOGGER_LOG") or \
    os.path.join(basedir, 'logs/data_logger.log')
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
