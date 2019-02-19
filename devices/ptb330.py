import serial
import json
import sys
from modules.threads import SerialThread, ConnectionType, SocketThread
from config import logger, Config

"""
Device specific constants for communication.
See device manual for more information
"""
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


def help_print():
    import ptb330
    print("Measurements per aquisition: {}".format(Config['measurement_qty']))
    module = Config['pressure_module']
    print("Pressure module ip: {0}".format(module['ip']))
    print("Pressure module port: {0}".format(module['port']))
    print(ptb330.__doc__)

class VaisalaPTB330(Config):
    def __init__(self, conn=ConnectionType.RS232, _serial_conn=None):
        self.queue = queue.Queue()
        self.conn = conn
        if self.conn is ConnectionType.RS232:
            sef.open_rs232_thread()
        elif self.conn is ConnectionType.SOCKET:
            sef.open_socket_thread()
        self.thread.daemon = True

    def open_socket_thread(self):
        self.thread = SocketThread(self.queue)

    def open_rs232_thread(self):
        self.thread = SerialThread(self.queue)

        if not _serial_conn:
            if serial_conn:
                ser = serial_conn
            else:
                ser = self.get_port()
        else:
            ser = _serial_conn
        self.open_connection(ser)
        self.process_serial()

    def open_connection(self, ser):
        try:
            if not self.thread.open_ser_connection(ser):
                self.thread.start()
        except SerialException as e:
            logger.error('Serial Exception', exc_info=True)
        except Exception as e:
            logger.error('EXCEPTION occured', exc_info=True)

    def write_device(self, data):
        self.thread.write_serial(data)

    def get_port(self):
        # find avaible connected serial devices
        available_ports = SerialThread.find_serial()
        print(available_ports)
        try:
            # test every available port for PTB330 device
            for port in available_ports:
                print("Trying connection on {}".format(port))
                if not int(port.split('COM')[1]) in [6]:
                    s = serial.Serial(port)
                    s.baudrate=19200
                    s.timeout=1
                    print("Serial out: {}".format(device_firmware.encode()))
                    sleep(.1)
                    s.flushInput()
                    s.flushOutput()
                    s.write((device_firmware+'\r').encode())
                    print("Trying reading")
                    sleep(.1)
                    resp = s.read(1000)
                    print(resp)
                    if "PTB330".encode() in resp:
                        s.close()
                        return port
                    s.close()
        except serial.SerialException as e:
            print(e)
        except Exception as e:
            print(e)



    def get_serial_number(self):
        return self.write(serial_number)

    def get_sensor_data(self, data):
       # device_list = data_output_format.strip('\"').split(';')
       # print(device_list)
       # print(data)
        for i, value in enumerate(data.split(";")[2:]):
         #   print(value)
            try:
                self.sensors[i].reading = value
                self.sensors[i].timestamp = 0
                send_data(self.sensors[i])
            except:
                pass

    def process_serial(self):
        while self.queue.qsize():
            try:
                data_in = self.queue.get().strip()
                if "PTB330 / 1.14" in data_in:
                    pass
                    #self.apply_sensor(data_in.lower())
                elif 'Serial number' in data_in:
                    self.device_SN = data_in.strip().split(":")[1].strip()
                   # print("device serial no : {}".format(self.device_SN))
                    device = {'id': self.device_SN, 'device': 'P_AVG'}
                    self.apply_sensor(device)
                elif data_in.find('serial') > 0:
                    module_id = data_in.strip().split(":")
                  #  print("module id : {}".format(module_id))
                    module_sensor_no = module_id[0].split(" ")[1]
                 #   print("module sn : {}".format(module_sensor_no))
                    module = {'id': module_id[1].strip(), 'device': 'P'+str(module_sensor_no)}
                    self.apply_sensor(module)
                elif self.sensing_mode:
                    self.get_sensor_data(data_in)
                else:
                    print(data_in)
            except queue.Empty:
                pass
        if self.repeater:
            threading.Timer(0.01, self.process_serial).start()
    def get_sensor_readings(self):
        self.write(reading)
    def get_sensor_types(self):
        self.write(sensor_descriptions)
        sleep(1)
    def apply_data_format(self):
        self.write(data_output_format)
        sleep(5)
        self.write(default_unit)
        sleep(5)
