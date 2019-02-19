# -*- coding: utf-8 -*-
#/usr/bin/python3

class Sensor():
    quantity = None
    reading = None
    timestamp = None
    unit = None
    id = None
    connection = None

    def __repr__(self):
        print(self.get_json_data())

    def get_json_data(self):
        return {"dev_rdg":self.reading,
            "dev_qty":self.quantity,
            "rdg_timestamp":self.timestamp,
            "dev_unit":self.unit,
            "dev_id":self.id,
            "conn":self.connection}
    """
    def apply_sensor(self, data):
        try:
            connected_sensor = Sensor()
            connected_sensor.unit = 'hPa'
            connected_sensor.id = data['id']
            connected_sensor.connection = data['device']
            connected_sensor.quantity =  MeasurementUnit(2).name
            #connected_sensor.__repr__()
            self.sensors.append(connected_sensor)
        except Exception as e:
            print("{}".format(e))
    """
