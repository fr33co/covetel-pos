import serial
import eventlet
from eventlet import wsgi
import httplib
import ftplib
import urllib
import SocketServer
import BaseHTTPServer
import time


class PosDisplay(object):

    def __init__(self):
        #self.ser = serial.Serial(2,baudrate=9600,bytesize=8, parity='N', timeout = None, stopbits=2, xonxoff=1, rtscts=1)
        #self.ser = serial.Serial(2,baudrate=9600,bytesize=8, parity='N', timeout = None, stopbits=2, xonxoff=1, rtscts=1)
        self.ser = serial.Serial(2,baudrate=9600,parity='N',bytesize=8,stopbits=1)
        #self.ser = serial.Serial(2,baudrate=9600)
        self.ser.write(" "*42)
        self.enviar_a_leds("OpenERP 6.1","PDVAL S.A.",0.1)

    def enviar_a_leds(self,linea1,linea2,timeout=0.001):
        for each in "\r"+linea1[:18]+"\n":
            self.ser.write(each)
            time.sleep(timeout)

        linea2 = linea2[:18]
        for each in "\r"+" "*(20-len(linea2))+linea2:
            self.ser.write(each)
            time.sleep(timeout)


    
    def bridge(self, env, start_response):
        self.ser.write(" "*42)
        linea1,linea2 = env['PATH_INFO'][1:].split("___")

        self.enviar_a_leds(linea1,linea2)

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['OK\r\n']

    def run(self):
        wsgi.server(eventlet.listen(('', 8100)), self.bridge)
        self.ser.close()

if __name__ == "__main__":
    pos_display = PosDisplay()
    pos_display.run()
