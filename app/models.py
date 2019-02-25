from datetime import datetime
from time import time
from flask import current_app
import jwt
from app import db
from app.basemodel import Base
import json

class Device(Base, db.Model):
    """Device database Model
    """
    #: database id
    id = db.Column(db.Integer, primary_key=True)
    #: device designation, used as identification id in POST query
    designation = db.Column(db.String(50), index=True, unique=True)
    serial_number = db.Column(db.String(100), index=True)
    #: short description of the device, maybe link to manual and purpose of use
    description = db.Column(db.String(200))
    #: device source ip address
    src_ip = db.Column(db.String(15), index=True)
    #: device source ip port
    src_port = db.Column(db.Integer, index=True)
    #: datastream destination URI
    dest_uri = db.Column(db.String(200), index=True)
    #: datastream format used to organise dest_uri params or data in POST query
    dest_format = db.Column(db.String(200))
    #: device reading interval in minutes
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
        """Server side data check before applying changes
        """
        print(data)
        self.from_dict(**data)
        db.session.add(self)
        db.session.commit()
        dev = Device.query.filter_by(designation=data['designation']).first()
