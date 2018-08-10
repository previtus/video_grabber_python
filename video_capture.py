import cv2
import numpy as np
from timeit import default_timer as timer
import datetime

class video_capture(object):
    """
    Generates individual frames from a stream of connected camera.
    Provides image when asked for.
    """

    def __init__(self, src=0):
        self.capture_handle = cv2.VideoCapture(src)

    def get_frame(self):
        start = datetime.datetime.now()

        ret, frame = self.capture_handle.read()

        end = datetime.datetime.now()
        fps = 1.0 / (end - start).total_seconds()
        return ret, frame, fps

    def destroy(self):
        self.capture_handle.release()
        cv2.destroyAllWindows()
