import cv2
from timeit import default_timer as timer

class video_capture(object):
    """
    Generates individual frames from a stream of connected camera.
    Provides image when asked for.
    """

    def __init__(self, src=0):
        self.capture_handle = cv2.VideoCapture(src)

    def get_frame(self):
        time_start = timer()

        ret, frame = self.capture_handle.read()

        time_end = timer()
        fps = 1.0 / (time_end - time_start)
        return ret, frame, fps

    def destroy(self):
        self.capture_handle.release()
        cv2.destroyAllWindows()
