import datetime
import subprocess
from csv import writer


class ShroomRoom():

    def __init__(self,
                 file_path: str,
                 max_c02: int,
                 min_c02: int,
                 max_temp: int,
                 min_temp: int,
                 max_hum: int,
                 min_hum: int):
        """
        """
        self.file_path = file_path
        self.max_c02 = max_c02
        self.min_c02 = min_c02
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_hum = max_hum
        self.min_hum = min_hum
        self._current_state = []

    def update_measurements(self):
        """
        read sensors in chamber and return list
        """
        current_time = datetime.now()
        current_time_str = current_time.strftime("%d/%m/%Y %H:%M:%S")
        self.current_state = [5, 3, 3, 3, 4, 5, 6, current_time_str]
        self.append_measurement()

    def upload_to_nextcloud(self):
        subprocess.call(["./upload.sh", self.file_path])

    def append_measurement(self):
        # Open file in append mode
        with open(self.file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(self._current_state)
        self.upload_to_nextcloud()
