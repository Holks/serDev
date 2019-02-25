from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from app import db
from app.main import bp
from app.main.forms import DeviceAddForm
from app.models import Device
import json

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
    data = Device.query.order_by(Device.id).all()
    form = DeviceAddForm()
    return render_template('main/device_list.html', form=form, data=data,
        header=Device._default_fields, heading='Devices')

@bp.route('/device', methods=['POST'])
def add_device():
    """Add device to database
    """
    json_obj = json.loads(request.form.get('form_json'))
    if Device.query\
            .filter_by(designation=json_obj['designation']).first():
        flash('please use a different designation')
    else:
        dev = Device()
        if dev.db_check(json_obj):
            flash('Added device {0}'.format(json_obj['designation']))
    return redirect(url_for('main.get_device_list'))

@bp.route('/device/<int:id>', methods=['GET', 'POST'])
def get_device(id):
    dev = Device.query.filter_by(id=json_obj['id']).first()
    return render_template('main/device_view.html', title='')
