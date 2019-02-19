# -*- coding: utf-8 -*-
#/usr/bin/python
import sys
import glob
import serial
from serial.serialutil import SerialException, SerialTimeoutException
import threading
import queue
import io

''' 
programm avad COM pordi, ootab seeriali sisendit loeb seni andmeid serialist kuni puhver tyhi
kontrollib QRkoodi pikkust ja CRC-d (vajalik kuna kasutusel demo programmiversioon, mis annad juhuslikult andmer2mpsu ja ka kui QR-kood on liialt riknenud, et ei ole enam loetav
loob m66tevahendi klassi objekti{tunnistus, kuup2ev, MVid, KlientID, crckood, ja v6ibolla veel midagi}
objekti saab hiljem kasutada defandmete t2itmiseks jms

''' 


class SerialThread(threading.Thread):    
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.data=None
        self.queue = queue
        
    def ava_seerial(self, ser):
        try:
            print( "Connecting " + str(ser['port']))
            self.conn = serial.Serial(ser['port'], ser['baudrate'], 
                bytesize=8, parity='N', stopbits=1,timeout=1)
            print(self.conn)
            self.sio = io.TextIOWrapper(io.BufferedReader(self.conn, 1), newline = '\r')
            #self.sio._CHUNK_SIZE = 1
            return False
        except Exception as e:
            raise e from None
            
    def write_serial(self, data):  
        self.data =  data +"\r"
    
    def read_serial(self):
        res = self.conn.readline()
        self.conn.flush()
       # if len(res) > 5 :                       # piirab igasuguse sodi sattumist seriali. Samas errorid peaksid läbi tulema.
        return res   
        
    def run(self):
        while True:
            try:                
                if self.conn.inWaiting(): 
                    text = self.sio.readlines()
                    for line in text:
                        if line and line.find('\x03') == -1:
                            self.queue.put(line.strip())
                    
                if self.data:
                    self.conn.write(self.data.encode())
                    self.data=None
                    #self.sio.flush()
            except:
                pass
        
def find_serial():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(50)] # otsib porte kuni 356-ni
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        result = []
        for port in ports:
            try: # exception if not available
                s = serial.Serial(port)
                s.close()   
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
