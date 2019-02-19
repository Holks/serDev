import serial
import json
import sys
from modules.threads import SerialThread
from modules.threads import SerialThread

"""
Datalog definitions
"""
aadress = "http://10.1.1.254/klm/?t=mootmine&tulem=0"
mv_id = ""
mv_tulem = ""
mv_valdkond = ""
aadress2 = "%20&k_stamp=0"
"""
Device specific constants for communication
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
 

class Sensor():
    quantity = None
    reading = None
    timestamp = None
    unit = None
    id = None
    connection = None

    def __repr__(self):
        print( {
            "rdg":self.reading,
            "qty":self.quantity,
            "timestamp":self.timestamp,
            "unit":self.unit,
            "id":self.id,
            "conn":self.connection
            })

            
class VaisalaPTB330():
    repeater = True
    sensors = []
    sensing_mode = False
    device_SN = None
    def __init__(self, port=None, baudrate=19200, timeout=3, \
        bytesize=8, parity='E', stopbits=1):
        self.queue = queue.Queue()
        self.thread = ser_thread.SerialThread(self.queue)
        self.thread.daemon = True
            
        print(port,baudrate)
        if not port:
            self.port = self.get_port()
        if self.port and baudrate:
            ser = {'port': self.port,'baudrate':baudrate}            
            self.open_connection(ser)  
            self.process_serial() 
            
    def open_connection(self, ser):
        try:
            if not self.thread.ava_seerial(ser): 
                self.thread.start() # käivitab seeriali lõime
        except SerialException:
            print("Serial error")
        except Exception as e:
            print("ERROR\n{0}".format(e))
        
    def write_serial(self, data):
        #print("data out '{}'".format(data))
        self.thread.write_serial(data)
    
    def write_socket(self, data):
        #print("data out '{}'".format(data))
        self.thread.write_serial(data)
        
    def get_port(self):
        available_ports = ser_thread.find_serial()
        print(available_ports)
        try:
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

 
class TesaSerialDevice(serial.Serial):
    def __repr__(self):
        return json.dumps(self.get_json(), sort_keys=True, indent=4)
    def get_json(self):
        return {'COM':self.port, 'baudrate':self.baudrate, \
            'protocol':str(self.bytesize)+str(self.parity)+str(self.stopbits)}
    def connect(self, queue):
        self.device = self.test_serial()
        self.thread = SerialThread(queue,ser=self.device)
        self.thread.daemon = True        
    def find_devices():
        """Function for searching available serial ports"""
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(50)]
        elif sys.platform.startswith('linux') \
            or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try: 
                s = TesaSerialDevice(port)
                s.close()   
                result.append(s)
            except (OSError, serial.SerialException):
                pass
        return result
    def test_serial(self):
        tt90 = TT20(port=self.port, baudrate=4800)
        tt90_in = tt90.getValue()
        if tt90_in != 'None':
            print("Using TT90\n")
            return tt90
        else:
            print("Using TESA MODUL\n")
            del(tt90)
            tt20 = TT20(port=self.port, baudrate=1200)
            return tt20
        pass
    def start_thread(self):
        self.thread.start()
    def get_connection(self):
        return json.dumps(self.get_json())
    def device_close(self):
        # TODO: close port
        print("Closing port {}".format(json.dumps(self.get_json())))        
        self.thread.join(timeout=0.1)
        self.device._conn.close()
        self.device = None
        
class TT20():
    def __init__(self, port, baudrate=4800):
        try:
            self._conn = serial.Serial(port=port, baudrate=baudrate,
                                  bytesize=7, parity='E', stopbits=2,
                                  timeout=0.5, xonxoff=0, rtscts=0)
        except  serial.SerialException as ex:
            print ("Port {0} is unavailable:".format(port, ex))
            self._conn.flush()
            self._conn.send_break()
            return    
    def write(self, data):
        sn = (('%s\r'%data).encode('utf-8')) 
        self._conn.write(sn)             
    def read(self):
        self._conn.setRTS(0) 
        res = self._conn.readline()
        self._conn.flush()
        if len(res) > 5 : 
            print(res)
            return clean(res)        
    def getValue(self):
        self.write("?")
        res = self.read()
        return str(res)    
    def waitValue(self):
        self._conn.setRTS(0)
        res = self._conn.readline()
        self._conn.flush()
        return str(clean(res))