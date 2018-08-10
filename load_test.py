from video_capture import video_capture
from renderer import renderer
from openface_handler import openface_handler
from data_saver import data_saver

data_saver = data_saver()
data_saver.load("testdata.h5")

data_saver.print_data()