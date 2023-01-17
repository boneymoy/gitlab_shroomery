from enum import Enum, IntEnum
from datetime import datetime
from csv import writer
import subprocess
import time

import RPi.GPIO as GPIO
import Adafruit_DHT
import mh_z19
import pigpio
import DHT22


class Pins(IntEnum):
    RELAIS_1 = 4
    LED_1 = 26
    SENSOR = 27

class Sensor(Enum):
    HUMIDITY = 'humidity'
    TEMPERATURE = 'temperature'
    CO2 = 'co2'

class ShroomRoom():

    def __init__(self,
                 file_path: str,
                 max_co2: int,
                 min_co2: int,
                 max_temp: int,
                 min_temp: int,
                 max_hum: int,
                 min_hum: int,
                 hum_sensor_pin: int,
                 co2_pin: int,
                 light_pin: int,
                 fan_pin: int):
        """
        """
        self.file_path = file_path
        self.max_co2 = max_co2
        self.min_co2 = min_co2
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_hum = max_hum
        self.min_hum = min_hum
        self.co2_pin = co2_pin
        self.light_pin = light_pin
        self.fan_pin = fan_pin
        self._last_action = 0
        self._adaptation_pause = 5 * 60 # 5 minuite
        self._current_state = {}
        self.initialize_pin(hum_sensor_pin)
        pi = pigpio.pi()
        self._dht22 = DHT22.sensor(pi, hum_sensor_pin)

    def initialize_pin(self, pin):
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(PINS.RELAIS_1.value, GPIO.OUT)
        # GPIO.setup(PINS.LED_1.value, GPIO.OUT)
        GPIO.setup(pin, GPIO.IN)

    def update_measurements(self):
        """
        read sensors in chamber and return list
        """
        sensor_data = self.read_sensor_data()
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # print(time)
        self._current_state = {
            'time': time,
            'humidity': sensor_data[Sensor.HUMIDITY],#sensor_data[Sensor.HUMIDITY],
            'temperature': sensor_data[Sensor.TEMPERATURE],#sensor_data[Sensor.TEMPERATURE],
            'co2': sensor_data[Sensor.CO2]['co2']
        }
        print(self._current_state)
        self.append_measurement()

    def upload_to_nextcloud(self):
        subprocess.call(["./upload.sh", self.file_path])
        print('uploaded')

    def append_measurement(self):
        # Open file in append mode
        with open(self.file_path, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow([
                self._current_state['time'],
                self._current_state['co2'],
                self._current_state['humidity'],
                self._current_state['temperature']
            ])

    def read_sensor_data(self):
        sensor_data = {}
        sensor_data[Sensor.CO2] = mh_z19.read_all()
        hum_temp_list = list(self._dht22.read())
        sensor_data[Sensor.HUMIDITY] = hum_temp_list[4]
        sensor_data[Sensor.TEMPERATURE] = hum_temp_list[3]
        return sensor_data

    def check_action(self):

        last_action_delta = time.time() - self._last_action
        if last_action_delta > self._adaptation_pause:
            if self._current_state['co2'] > self.max_co2:
                # start fan
                pass
            elif self._current_state['co2'] < self.min_co2:
                # is this possible
                pass
            if self._current_state['temperature'] > self.max_temp:
                # fan if temp outside is cooler
                pass
            elif self._current_state['temperature'] < self.min_temp:
                # heat up
                pass
            if self._current_state['humidity'] > self.max_hum:
                # start fan
                pass
            elif self._current_state['humidity'] < self.min_hum:
                # start humidifier 
                pass
