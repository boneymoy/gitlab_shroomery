from datetime import datetime
from csv import writer

import time
import subprocess


FILE_PATH = 'measurement.csv'


def upload_to_nextcloud(path: str):
    subprocess.call(["./upload.sh", path])


def append_measurement(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
    upload_to_nextcloud(file_name)


while True:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%d/%m/%Y %H:%M:%S")
    append_measurement(FILE_PATH, [5, 3, 3, 3, 4, 5, 6, current_time_str])
    time.sleep(10)
