# /usr/bin/env python3

# pip install flask-socketio
from flask import Flask, url_for, request, send_from_directory

import json
import sys

import threading
import time
from datetime import datetime
from multiprocessing import Lock

mutex = Lock()

# pip install pyserial
import serial


class ArduinoManager:
    connection = None
    serial_port = None
    baud_rate = None
    retry_timer = 0.02 # time to wait between trying to poll for data
    wait_timeout = 0.005 # time to wait in ms when polling for data
    valid_sensors = []
    timer = None
    log = [{"sensor":"TEST","message":"test1","timestamp":"2015-08-30 01:30:33"},
           {"sensor":"TEST","message":"test2","timestamp":"2015-08-30 01:31:33"},
           {"sensor":"TEST","message":"test3","timestamp":"2015-08-30 01:32:33"}]

    def __init__(self, baud_rate=9600, serial_port='/dev/tty.usbserial'):
        global mutex
        self.baud_rate = baud_rate
        self.serial_port = serial_port
        with mutex:
            self.setup_arduino()
            self.timer = threading.Timer(self.retry_timer, self.get_from_arduino)

    def shutdown(self):
        global mutex
        with mutex:
            try:
                if self.connection:
                    self.connection.close()
            except:
                e = sys.exc_info()[0]
                print(e)

            try:
                if self.timer:
                    self.timer._stop()
            except:
                e = sys.exc_info()[0]
                print(e)

    def setup_arduino(self):
        try:
            self.connection = serial.Serial(self.serial_port, self.baud_rate, self.wait_timeout)
            # set the reset signal
            self.connection.setDTR( level=False ) 
            time.sleep(2)
            # don't do anything here which might overwrite the Arduino's program
            self.connection.setDTR( level=True )  # remove the reset signal, the Arduino will restart
            line = self.connection.readline().decode("utf-8")
            self.valid_sensors = line.split(",")
        except:
            e = sys.exc_info()[0]
            print("setup_arduino exception: " + str(e))
        self.valid_sensors += ["ALL","TEST"]

    def send_to_arduino(self, message):
        if self.connection:
            try:
                global mutex
                with mutex:
                    self.connection.write(message.encode("utf-8"))
                    return True
            except:
                e = sys.exc_info()[0]
                print("send_to_arduino exception: " + str(e))
                return False

    def get_from_arduino(self):
        try:
            global mutex
            with mutex:
                line = self.connection.readline().decode("utf-8")
                if line:
                    tmp = line.split(",")
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.log.append({"sensor":tmp[0],"message":tmp[1:], "timestamp": now})
        except:
            e = sys.exc_info()[0]
            print("get_from_arduino exception: " + str(e))

    def get_arduino_log(self,sensor="ALL"):
        global mutex
        with mutex:
            if sensor == "ALL":
                return [x["timestamp"] + "," + x["sensor"] + "," + x["message"] for x in self.log]
            else:
                return [x["timestamp"] + "," + x["sensor"] + "," + x["message"] for x in self.log if x["sensor"] == sensor]

    def get_sensors(self):
        pass

    def validate_sensor(self, sensor):
        global mutex
        with mutex:
            if sensor in self.valid_sensors:
                return sensor
            else:
                print("Invalid sensor specified, available sensors are: " + ",".join(self.valid_sensors))
                return ""


def validate_data(data):
    return data

# Create server application and Arduino manager

am = None
app = Flask(__name__,static_url_path='')

# Webserver begins here

# return the index page
@app.route('/', methods=['GET'])
def index():
    #return """<html><body><h1>Hi there!</h1></body></html>"""
    return app.send_static_file('index.html')

# Send data to specified sensor
#  data : data to send to the sensor, should be formated in a way that the arduino expects
@app.route('/send/<sensor>', methods=['POST'])
def send(sensor):
    global am
    data = request.json.get('data', "")
    sensor = am.validate_sensor(sensor)
    data = validate_data(data)
    if not len(sensor):
        return json.dumps({"sensor":sensor,"data":data,"success":False}), 520

    print("Sending: [" + sensor + ":" + data + "] to arduino")
    ret = am.send_to_arduino(sensor + ":" + data)

    if not ret:
        return json.dumps({"sensor":sensor,"data":data,"success":False}), 520

    return json.dumps({"sensor":sensor,"data":data,"success":True}), 200


# Get list of timestamped events for the sensor specified
@app.route('/get/<sensor>', methods=['GET'])
def get(sensor):
    global am
    sensor = am.validate_sensor(sensor)
    data = am.get_arduino_log(sensor)

    if len(data) == 0:
        return json.dumps({"sensor":sensor,"success":False}), 520

    return json.dumps({"sensor":sensor,"data":data,"success":True}), 200

# MAIN: start the server
if __name__ == '__main__':
    # start_process('loop',  './loop')
    am = ArduinoManager()
    app.run(debug=True,host='0.0.0.0')
