import time
from shroom_room import ShroomRoom
from logic_functions import append_measurement

UPDATE_FREQ = 10

FILE_PATH_INC = 'incubation_chamber.csv'
FILE_PATH_FRT = 'fruiting_chamber.csv'
incubation_chamber = ShroomRoom(FILE_PATH_INC,
                                10,
                                10,
                                10,
                                10,
                                10,
                                10)
fruiting_chamber = ShroomRoom(FILE_PATH_FRT,
                              20,
                              20,
                              20,
                              20,
                              20,
                              20)

while True:
    time.sleep(UPDATE_FREQ)
    incubation_chamber.update_measurements()
    fruiting_chamber.update_measurements()
