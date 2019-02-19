# -*- coding: utf-8 -*-
#/usr/bin/python3
import os

class Config:

    serial_conn = json.loads(os.environ.get("PRESSURE_MODULE_SERIAL_CONN")) \
        or {'baudrate':19200, 'bits':8, 'parity':'N', 'stop_bits': 2}
    pressure_module = json.loads(os.environ.get("PRESSURE_MODULE")) or {'ip':'10.1.1.73', 'port':24}

    device_info = "?"
    serial_number = "SNUM"
    device_firmware = "VERS"
    device_date = "DATE"
    readings_w_datetime = "S1"
    reading = "SEND"
    sensor_descriptions = "form ??"
    set_form = "FORM"
    data_output_format = 'date ";" time ";" P ";" P1 ";" P2 #RN'
    default_output_format = "form /"
    default_unit = "UNIT hPa"
    units = [b'\xd1\x88C'.decode(),'%H','mb', 'hPa']

DATABASE_CONFIG = {
        'base_uri' : "http://10.1.1.254/klm/?t=mootmine&tulem=0"
        'dev_id' : ""
        'dev_rdg' : ""
        'dev_qty' : ""
        'rdg_timestamp's : "%20&k_stamp=0"
}
