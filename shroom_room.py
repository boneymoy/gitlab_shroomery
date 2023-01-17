from datetime import datetime
from csv import writer

import multiprocessing
import subprocess
import traceback
import logging
import time
import sys

import RPi.GPIO as GPIO
import mh_z19
import pigpio
import DHT22


class ShroomRoom():

    def __init__(self,
                 name: str,
                 file_path: str,
                 limits: dict,
                 pins: dict):
        """
        """
        self.name = name
        self.file_path = file_path
        self.limits = limits
        self.pins = pins
        self.fan_runtime = 10  # in s
        self._last_action = time.time()
        self._adaptation_pause = 1 * 10 # in seconds
        self._current_state = {}
        self.initialize_pins()
        logging.basicConfig(filename=f'{self.name}.log',
                            encoding='utf-8',
                            level=logging.DEBUG)
        logging.info(f'{self.name} is online.')
        # temp and humidity sensor

    def initialize_pins(self):
        GPIO.setmode(GPIO.BCM)
        # print(self.pins['fan_in'])
        GPIO.setup(self.pins['fan_in'], GPIO.OUT)
        GPIO.setup(self.pins['heater'], GPIO.OUT)
        GPIO.output(self.pins['fan_in'], GPIO.LOW)
        GPIO.setup(self.pins['fan_out'], GPIO.OUT)
        GPIO.output(self.pins['fan_out'], GPIO.LOW)
        # GPIO.setup(PINS.LED_1.value, GPIO.OUT)
        GPIO.setup(self.pins['hum'], GPIO.IN)
        pi = pigpio.pi()

    def update_measurements(self):
        """
        read sensors in chamber and return list
        """
        sensor_data = self.read_sensor_data()
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._current_state = {
            'time': time,
            'hum': sensor_data['hum'],
            'temp': sensor_data['temp'],
            'co2': sensor_data['co2']
        }
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
                self._current_state['hum'],
                self._current_state['temp']
            ])

    def read_sensor_data(self):
        sensor_data = {}
        try:
            sensor_data['co2'] = mh_z19.read_all()['co2']
        except Exception as e:
            logging.error(f'Error reading CO2 Sensor.')
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[2])
        # hum_temp_list = list(self._dht22.read())
        # humidity, temperature = DHT22.read_DHT(self.pins['hum'])
        humidity = 22
        temperature = 22
        sensor_data['hum'] = humidity
        sensor_data['temp'] = temperature
        return sensor_data

    def check_action(self):
        """
        check if every measurement lies in defined limits
        !!! start function in parallel !!!

        co2>limit -> ventilation
        co2<limit -> nothing

        hum<limit -> humidifier
        hum>limit -> ventilation?

        temp<limit-> heater
        temp>limit-> ventilation
        """
        last_action_delta = time.time() - self._last_action
        if last_action_delta > self._adaptation_pause:
            if self._current_state['co2'] > self.limits['co2']['max']:
                # turn on ventilation 
                logging.info(f'CO2 too high \n{self._current_state}  -->  start ventilation!')
                self.switch_relay(
                    pins=[self.pins['fan_in'],
                          self.pins['fan_out']],
                    on_time=self.fan_runtime)
                self._last_action = time.time()
            if self._current_state['hum'] < self.limits['hum']['min']:
                logging.info(f'Humidity too low \n {self._current_state} -->  start humidifier')
                # turn on humidifier
                self.switch_relay(
                    pins=[self.pins['hum']],
                    on_time=self.fan_runtime)
                self._last_action = time.time()
            if self._current_state['hum'] > self.limits['hum']['max']:
                logging.info(f'Humidity too high \n {self._current_state} -->  start ventilation!')
                # turn on ventilation 
                self.switch_relay(
                    pins=[self.pins['fan_in'],
                          self.pins['fan_out']],
                    on_time=self.fan_runtime)
                self._last_action = time.time()
            if self._current_state['temp'] < self.limits['temp']['min']:
                logging.info(f'Temperature too low \n {self._current_state} -->  start heater!')
                # turn on heater 
                self.switch_relay(
                    pins=[self.pins['heat']],
                    on_time=self.fan_runtime)
                self._last_action = time.time()
            if self._current_state['temp'] > self.limits['temp']['max']:
                logging.info(f'Temperature too high \n {self._current_state} -->  start ventilation!')
                # turn on ventilation 
                self.switch_relay(
                    pins=[self.pins['heater']],
                    on_time=self.fan_runtime)
                self._last_action = time.time()

    def switch_relay(self, pins: list, on_time: int):
        """
        turn on device at realy pins defined in list
        keep device turned on for on_time seconds
        """
        start_time = time.time()
        for pin in pins:
            GPIO.output(pin, GPIO.HIGH)
        current_time = time.time()
        while current_time - start_time < on_time:
            current_time = time.time()
            continue
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)

    def stop(self):
        GPIO.output(self.pins['fan_in'], GPIO.LOW)
        GPIO.output(self.pins['fan_out'], GPIO.LOW)
        GPIO.output(self.pins['heater'], GPIO.LOW)
        logging.info(f'{self.name} turned off!')
