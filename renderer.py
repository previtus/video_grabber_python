import cv2
import numpy as np
from timeit import default_timer as timer
import datetime, time
from threading import Thread

class renderer(object):
    """
    Draw image to screen.
    """

    def __init__(self, video_capture, openface_handler, data_saver):
        # Init stuff

        self.video_capture = video_capture
        self.openface_handler = openface_handler
        self.data_saver = data_saver

        self.sample_every = 1 # sec


        return None

    def show_frames(self):
        time_start = timer()
        while (True):
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if key == ord('8'):
                self.sample_every /= 2
            if key == ord('2'):
                self.sample_every *= 2

            ret, frame, fps = self.video_capture.get_frame()

            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.putText(frame, "FPS "+'{:.2f}'.format(fps)+", sample rate "+'{:.3f}'.format(self.sample_every), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            time_now = timer()
            if (time_now - time_start) > self.sample_every:
                time_start = time_now

                # HERE DO SOMETHING WITH THE IMAGE (every self.sample_every sec)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('frame', frame)



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

    def runopenface_on_frames_everytick(self, show=True, tick=1):
        self.sample_every = tick

        time_start = timer()
        while (True):
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            if key == ord('8'):
                self.sample_every /= 2.0
            if key == ord('2'):
                self.sample_every *= 2.0

            ret, frame, fps = self.video_capture.get_frame()

            time_now = timer()
            if (time_now - time_start) > self.sample_every:
                time_start = time_now

                timestamp = time.time()
                time_value = datetime.datetime.fromtimestamp(timestamp)
                print(time_value.strftime('%Y-%m-%d %H:%M:%S'))

                # HERE DO SOMETHING WITH THE IMAGE (every self.sample_every sec)
                #passed, rep, bb = self.openface_handler.getRep(frame)
                successes, reps, bbs = self.openface_handler.getRepMulti(frame)
                for i, passed in enumerate(successes):
                    if passed:
                        if passed:
                            rep = reps[i]
                            bb = bbs[i]
                            #print(rep)
                            cv2.rectangle(frame, (bb.left(), bb.top()), (bb.right(), bb.bottom()), (255, 0, 0), 2)

                            self.data_saver.add_record(timestamp, rep)

                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Expansive saving, maybe limit?
                self.data_saver.save()


            cv2.putText(frame, "FPS "+'{:.2f}'.format(fps)+", sample rate "+'{:.3f}'.format(self.sample_every), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if show:
                cv2.imshow('frame', frame)

"""
    def runopenface_on_frames_nowaiting(self, show=True):
        while (True):
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

            time_start = timer()

            ret, frame, _ = self.video_capture.get_frame()

            # always
            if True:
                #passed, rep, bb = self.openface_handler.getRep(frame)
                successes, reps, bbs = self.openface_handler.getRepMulti(frame)
                for i, passed in enumerate(successes):
                    if passed:
                        if passed:
                            rep = reps[i]
                            bb = bbs[i]
                            print(rep)
                            cv2.rectangle(frame, (bb.left(), bb.top()), (bb.right(), bb.bottom()), (255, 0, 0), 2)
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            time_end = timer()
            fps = 1.0 / (time_end - time_start)

            cv2.putText(frame, "FPS "+'{:.2f}'.format(fps)+", sample rate "+'{:.3f}'.format(self.sample_every), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if show:
                cv2.imshow('frame', frame)
"""