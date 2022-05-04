import sys
import time
import traceback
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

from shroom_room import ShroomRoom

UPDATE_FREQ = 5
UPLOAD_FREQ = 15
ACTION_FREQ = 30

FILE_PATH_INC = 'incubation_chamber.csv'
FILE_PATH_FRT = 'fruiting_chamber.csv'


def monitor_loop(shroom_room):
    last_update_time = time.time()
    last_upload_time = time.time()
    while True:
        current_time = time.time()
        if current_time - last_update_time > UPDATE_FREQ:
            print("update")
            shroom_room.update_measurements()
            last_update_time = time.time()
        if current_time - last_upload_time > UPLOAD_FREQ:
            shroom_room.upload_to_nextcloud()
            last_upload_time = time.time()


def controller_loop(shroom_room):
    last_action_time = time.time()
    while True:
        current_time = time.time()
        if current_time - last_action_time > ACTION_FREQ:
            shroom_room.check_action()
            last_action_time = time.time()


try:
    BaseManager.register('ShroomRoom', ShroomRoom)
    manager = BaseManager()
    manager.start()
    incubation_chamber = manager.ShroomRoom(
        file_path=FILE_PATH_INC,
        limits={
            'co2': {
                'max': 800,
                'min': 0
            },
            'temp': {
                'max': 40,
                'min': 0
            },
            'hum': {
                'max': 100,
                'min': 0
            }
        },
        pins={
            'hum': 4,
            'co2': 1,
            'light': 1,
            'fan': 1,
        })

    Process(target=monitor_loop, args=[incubation_chamber]).start()
    Process(target=controller_loop, args=[incubation_chamber]).start()

except Exception as e:
    print('Error in main loop')
    print(e)
    print(traceback.format_exc())
    print(sys.exc_info()[2])
