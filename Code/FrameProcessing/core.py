import cv2
from projectutils import play_video,count_cars

video_file = '/home/shrobon/Desktop/Computer Vision Project/Dataset/input/in%6d.jpg' #ground truth 
window_name= "Target Video" 
#play_video(video_file,25,window_name)
#count_cars(video_file,sleepTime,x1,y1,x2,y2,trim_begin,trim_end,display_window_name)
count_cars(video_file,25,0,0,0,0,0,0,window_name)