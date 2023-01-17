import traceback
import threading
import time
import sys

from shroom_room import ShroomRoom

UPDATE_FREQ = 10
UPLOAD_FREQ = 30
ACTION_FREQ = 60

FILE_PATH_INC = 'incubation_chamber.csv'
FILE_PATH_FRT = 'fruiting_chamber.csv'


def monitor_loop(shroom_room):
    last_update_time = time.time()
    last_upload_time = last_update_time
    last_action_time = last_update_time
    while True:
        current_time = time.time()
        if current_time - last_update_time > UPDATE_FREQ:
            print("update")
            shroom_room.update_measurements()
            print(shroom_room._current_state)
            last_update_time = time.time()
        if current_time - last_upload_time > UPLOAD_FREQ:
            shroom_room.upload_to_nextcloud()
            last_upload_time = time.time()
        if current_time - last_action_time > ACTION_FREQ:
            shroom_room.check_action()
            last_action_time = time.time()

if __name__ == "__main__":
    try:
        incubation_chamber = ShroomRoom(
            name = 'Incubation Chamber',
            file_path=FILE_PATH_INC,
            limits={
                'co2': {
                    'max': 1000,
                    'min': 0
                },
                'temp': {
                    'max': 30,
                    'min': 0
                },
                'hum': {
                    'max': 80,
                    'min': 0
                }
            },
            pins={
                'hum': 17,
                'co2': 1,
                'light': 1,
                'fan_in': 19,
                'fan_out': 13,
                'heater': 10
            })
        rooms = []
        rooms.append(incubation_chamber)
        for room in rooms:
            monitor_loop(room)

    except (Exception, KeyboardInterrupt) as e:
        for room in rooms:
            room.stop()
        print('Error in main loop')
        print(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
