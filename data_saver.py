import numpy as np
import h5py
import datetime

class data_saver(object):
    """
    holds and saves the data
    """

    def __init__(self):

        self.times_data = []
        self.saved_data = []

        return None

    def add_record(self, time_time, data_repr):
        self.times_data.append(time_time)
        self.saved_data.append(data_repr)

    def save(self, filename="default_data.h5"):
        with h5py.File(filename, 'w') as hf:
            hf.create_dataset("times_data", data=self.times_data)
            hf.create_dataset("saved_data", data=self.saved_data)

    def load(self, filename="default_data.h5"):
        with h5py.File(filename, 'r') as hf:
            self.times_data = hf['times_data'][:]
            self.saved_data = hf['saved_data'][:]

    def print_data(self):
        for i in range(0,len(self.times_data)):

            time_value = datetime.datetime.fromtimestamp(self.times_data[i])
            print(time_value.strftime('%Y-%m-%d %H:%M:%S'))

            print(self.saved_data[i])