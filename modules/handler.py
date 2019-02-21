# -*- coding: utf-8 -*-
#/usr/bin/python3

from config import DATABASE_CONFIG as config
import time, urllib.request

def send_data_klm(data):
  uri = config['base_uri'] \
    + "%20" \
    + data['dev_id'].strip(' ') \
    + "%20" \
    + str(data['dev_rdg'].replace(',','.')).strip(' ') \
    + "%20" \
    + str(data['dev_qty'].strip(' ')) \
    + "%20" \
    + str(config['rdg_timestamp'])
  response = urllib.request.urlopen(uri)
  if DEBUG:
    print(uri+str(response.read()))
