from datetime import datetime
from time import time
from flask import current_app
import jwt
from app import db
from app.basemodel import Base


class Device(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(140))
    ip = db.Column(db.String(64), index=True)
    port = db.Column(db.Integer, index=True)

    _default_fields = [
        'designation',
        'ip',
        'port'
    ]
