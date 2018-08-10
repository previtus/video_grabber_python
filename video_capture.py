import cv2
import numpy as np
from timeit import default_timer as timer
from threading import Thread
from imutils.video import FPS

class video_capture(object):
    """
    Generates individual frames from a stream of connected camera.
    Provides image when asked for.
    """

    def __init__(self, src=0):
        self.capture_handle = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.capture_handle.read()

        self.stopped = False
        self.fps = 0

    def get_frame_direct(self):
        fps = FPS().start()
        ret, frame = self.capture_handle.read()
        fps.update()
        fps.stop()

        return ret, frame, fps.fps()

    def destroy(self):
        self.stop()
        self.capture_handle.release()
        cv2.destroyAllWindows()

    # threading functions
    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            fps = FPS().start()
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.capture_handle.read()
            fps.update()
            fps.stop()
            #self.fps = fps.fps()

            if fps.elapsed() == 0:
                self.fps = 0.0
            else:
                self.fps = fps._numFrames / fps.elapsed()

    def read(self):
        # return the frame most recently read
        return self.frame, self.fps

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
