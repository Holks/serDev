from datetime import datetime
from time import time
from flask import current_app
import jwt
from app import db
from app.basemodel import Base


class Device(Base, db.Model):
    """Device database Model
    id
        database id

    designation
        device designation, used as
         identification id in POST query

    serial_number
        device serial number

    description
        short description of the device,
        maybe link to manual
        and purpose of use

    src_ip
        device source ip address

    src_port
        device source ip port

    dest_uri
        datastream destination URI

    dest_format
        datastream format used to organise
        dest_uri params or data in POST query

    rgd_interval
        device reading interval in minutes
    """
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(50), index=True, unique=True)
    serial_number = db.Column(db.String(100), index=True)
    description = db.Column(db.String(200))
    src_ip = db.Column(db.String(15), index=True)
    src_port = db.Column(db.Integer, index=True)
    dest_uri = db.Column(db.String(200), index=True)
    dest_format = db.Column(db.String(200))
    rgd_interval = db.Column(db.Integer)

    _default_fields = [
        'designation',
        'serial_number',
        'src_ip',
        'src_port',
        'dest_uri',
        'dest_format',
        'rgd_interval'
    ]

    def db_check(self, data):
        print(data)
