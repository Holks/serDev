from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, \
    IPAddress, NumberRange, URL

class DeviceAddForm(FlaskForm):
    designation = StringField('Designation', validators=[DataRequired(),
        Length(max=50)], render_kw={"placeholder": "Designation"})
    description = TextAreaField('Description', validators=[Length(max=200)],
        render_kw={"placeholder": "Desription", "cols":"50", "rows":"3"})
    src_ip = StringField('Source IP address', validators=[DataRequired(),
        IPAddress()], render_kw={"placeholder": "IP address"})
    src_port = IntegerField('Source IP port', validators=[DataRequired(),
        NumberRange(min=1,max=65535)], render_kw={"placeholder": "IP port"})
    dest_uri = StringField('Destination URL',
        validators=[DataRequired(), URL()],
        render_kw={"placeholder": "Destination URL"})
    dest_format = StringField('Destination format',
        render_kw={"placeholder": "Format"})
    rdg_interval = IntegerField('Reading interval', validators=[DataRequired()],
        render_kw={"placeholder": "Interval [min]"})
