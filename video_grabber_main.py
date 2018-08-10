from video_capture import video_capture
from renderer import renderer
from openface_handler import openface_handler
from data_saver import data_saver

video_capture = video_capture()
openface_handler = openface_handler()
data_saver = data_saver()
renderer = renderer(video_capture, openface_handler, data_saver)

#renderer.show_frames()

tick = 1 # every ten seconds!

renderer.runopenface_on_frames_everytick(show=True,tick=tick)
#renderer.runopenface_on_frames_nowaiting(show=True)
#renderer.record_frames()


video_capture.destroy()




