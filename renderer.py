import cv2
import numpy as np
from timeit import default_timer as timer
from threading import Thread

class renderer(object):
    """
    Draw image to screen.
    """

    def __init__(self, video_capture):
        # Init stuff

        self.video_capture = video_capture
        return None

    def show_frames(self):
        while (True):
            ret, frame, fps = self.video_capture.get_frame()

            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.putText(frame, "FPS "+'{:.2f}'.format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


"""
    def record_frames(self):

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

        while (self.video_capture.capture_handle.isOpened()):
            ret, frame = self.video_capture.get_frame()
            if ret == True:
                frame = cv2.flip(frame, 0)

                # write the flipped frame
                out.write(frame)

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        out.release()
"""