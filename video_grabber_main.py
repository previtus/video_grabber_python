from video_capture import video_capture
from renderer import renderer
from openface_handler import openface_handler

video_capture = video_capture()
openface_handler = openface_handler()
renderer = renderer(video_capture, openface_handler)

#renderer.show_frames()
renderer.runopenface_on_frames(show=True)
#renderer.record_frames()


video_capture.destroy()




