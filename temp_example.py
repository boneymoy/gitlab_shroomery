"""
Remember to start the daemon with the command
'sudo pigpiod' before running this script. It
needs to be restarted every time your pi
is restarted.
"""

import pigpio
import DHT22
from time import sleep

# Initiate GPIO for pigpio
pi = pigpio.pi()
# Setup the sensor
dht22 = DHT22.sensor(pi, 4) # use the actual GPIO pin name

while True:
    print(list(dht22.read()))
    sleep(3)


