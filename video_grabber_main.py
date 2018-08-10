from video_capture import video_capture
from renderer import renderer

video_capture = video_capture()
renderer = renderer(video_capture)

renderer.show_frames()
#renderer.record_frames()


video_capture.destroy()




