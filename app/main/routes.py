from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.main import bp
from app.main.forms import DeviceForm
from app.models import Device

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """Index page to be served to client
    """
    return render_template('index.html', title='serDev')

@bp.route('/device', methods=['GET'])
def get_device_list():
    """Get list of devices from database
    """
    form = DeviceForm()
    return render_template('main/device.html', form=form, heading='Devices')

@bp.route('/device', methods=['POST'])
def add_device():
    """Add device to database
    """
    form = request.form
    dev = Device()
    if dev.db_check(form):
        pass
    return redirect(url_for('main.get_device_list'))
