#!/bin/sh
""" This script is used to boot a Docker container """

source ~/aquisitor/venv/bin/activate

"""
Launch gunicorn:
- listen on port 5000
- access log to stderr
- error log to stderr
"""
exec gunicorn -b :5000 --access-logfile - --error-logfile - aquisitor:app
