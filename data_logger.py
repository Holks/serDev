# -*- coding: utf-8 -*-
#/usr/bin/python3

from modules.handler import send_data_klm
from devices import ptb330
from config import logger


if __name__ == "__main__":
    sensors = []
    try:
        for sensor in sensors:
            send_data_klm(sensor.get_json_data())
    except Exception as e:
        logger.error('EXCEPTION occured', exc_info=True)
