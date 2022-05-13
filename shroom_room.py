from datetime import datetime
from csv import writer
import multiprocessing
import subprocess
import time

import RPi.GPIO as GPIO
import mh_z19
import pigpio
import DHT22


class ShroomRoom():

    def __init__(self,
                 file_path: str,
                 limits: dict,
                 pins: dict):
        """
        """
        self.file_path = file_path
        self.limits = limits
        self.pins = pins
        self.fan_runtime = 10  # in s
        self._last_action = time.time()
        self._adaptation_pause = 1 * 60  # 1 minuite
        self._current_state = {}
        self.initialize_pins()
        # temp and humidity sensor

    def initialize_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins['fan'], GPIO.OUT)
        # GPIO.setup(PINS.LED_1.value, GPIO.OUT)
        GPIO.setup(self.pins['hum'], GPIO.IN)
        pi = pigpio.pi()
        self._dht22 = DHT22.sensor(pi, self.pins['hum'])

    def update_measurements(self):
        """
        read sensors in chamber and return list
        """
        sensor_data = self.read_sensor_data()
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # print(time)
        self._current_state = {
            'time': time,
            'hum': sensor_data['hum'],
            'temp': sensor_data['temp'],
            'co2': sensor_data['co2']
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
                self._current_state['hum'],
                self._current_state['temp']
            ])

    def read_sensor_data(self):
        sensor_data = {}
        #TODO
        sensor_data['co2'] = mh_z19.read_all()['co2']
        hum_temp_list = list(self._dht22.read())
        sensor_data['hum'] = hum_temp_list[4]
        sensor_data['temp'] = hum_temp_list[3]
        return sensor_data

    def check_action(self):
        """
        check if every measurement lies in defined limits
        !!! start function in parallel !!!
        """
        # TODO
        last_action_delta = time.time() - self._last_action
        print(last_action_delta)
        if last_action_delta > self._adaptation_pause:
            if self._current_state['co2'] > self.limits['co2']['max']:
                # threading.Thread(self.start_fan())
                fan_process = multiprocessing.Process(target=self.start_fan())
                fan_process.start()
                self._last_action = time.time()

    def start_fan(self):
        """
        switch relais so fan is started
        """
        start_time = time.time()
        # GPIO.output(self.pins['fan'], GPIO.HIGH)
        current_time = time.time()
        print('turned on')
        while current_time - start_time < self.fan_runtime:
            time.sleep(1)
            current_time = time.time()
            continue
        print('turned off')
        # GPIO.output(self.pins['fan'], GPIO.LOW)

    def turn_off(self):
        GPIO.output(self.pins['fan'], GPIO.LOW)
