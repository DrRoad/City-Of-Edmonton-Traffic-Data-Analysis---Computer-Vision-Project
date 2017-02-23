import cv2
from projectutils import play_video,count_cars

video_file = '../Dataset/StAlbert/traffic_south.MP4'
window_name= "Target Video" 
play_video(video_file,25,window_name)
count_cars(video_file,25,window_name)