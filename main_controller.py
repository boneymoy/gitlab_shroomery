import time
from shroom_room import ShroomRoom

UPDATE_FREQ = 1
UPLOAD_FREQ = 5
CONTROL_FREQ = 5

FILE_PATH_INC = 'incubation_chamber.csv'
FILE_PATH_FRT = 'fruiting_chamber.csv'
incubation_chamber = ShroomRoom(file_path=FILE_PATH_INC,
                                max_co2=10,
                                min_co2=10,
                                max_temp=10,
                                min_temp=10,
                                max_hum=10,
                                min_hum=10,
                                hum_sensor_pin=4,
                                co2_pin=1,
                                light_pin=1,
                                fan_pin=1)
rooms = [incubation_chamber]

last_update_time = time.time()
last_upload_time = time.time()
last_control_time = time.time()
print("Init done.")
while True:
    current_time = time.time()
    if current_time - last_update_time > UPDATE_FREQ:
        print("update")
        for room in rooms:
            room.update_measurements()
        last_update_time = time.time()
    if current_time - last_upload_time > UPLOAD_FREQ:
        for room in rooms:
            room.upload_to_nextcloud()
        last_upload_time = time.time()
    if current_time - last_control_time > CONTROL_FREQ:
        for room in rooms:
            room.check_action()
    # print(incubation_chamber._current_state)
    # fruiting_chamber.update_measurements()
    # fruiting_chamber.upload_to_nextcloud()
