import sys
import time
import traceback
import threading

from shroom_room import ShroomRoom

UPDATE_FREQ = 5
UPLOAD_FREQ = 15
ACTION_FREQ = 30

FILE_PATH_INC = 'incubation_chamber.csv'
FILE_PATH_FRT = 'fruiting_chamber.csv'


def monitor_loop(shroom_room):
    last_update_time = time.time()
    last_upload_time = time.time()
    last_action_time = time.time()
    while True:
        current_time = time.time()
        if current_time - last_update_time > UPDATE_FREQ:
            print("update")
            shroom_room.update_measurements()
            last_update_time = time.time()
        if current_time - last_upload_time > UPLOAD_FREQ:
            shroom_room.upload_to_nextcloud()
            last_upload_time = time.time()
        if current_time - last_action_time > ACTION_FREQ:
            shroom_room.check_action()
            last_action_time = time.time()

if __name__ == "__main__":
    try:
        # BaseManager.register('ShroomRoom', ShroomRoom)
        # manager = BaseManager()
        # manager.start()
        incubation_chamber = ShroomRoom(
            name = 'Incubation Chamber',
            file_path=FILE_PATH_INC,
            limits={
                'co2': {
                    'max': 600,
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
                'fan_in': 19,
                'fan_out': 13,
                'heater': 10
            })
        rooms = []
        rooms.append(incubation_chamber)
        for room in rooms:
            monitor_loop(room)
        # Process(target=monitor_loop, args=[incubation_chamber]).start()
        # Process(target=controller_loop, args=[incubation_chamber]).start()

    except (Exception, KeyboardInterrupt) as e:
        for room in rooms:
            room.stop()
        print('Error in main loop')
        print(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
