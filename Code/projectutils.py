import cv2


#To display the target video
def play_video(video_file,sleepTime,display_window_name):
	
	cv2.namedWindow(display_window_name)
	cap = cv2.VideoCapture(video_file)
	while(cap.isOpened()):
		#reading frame by frame
		ret, frame = cap.read()

		cv2.imshow(display_window_name,frame)

		#Video stops playing if 'q' or escapse is pressed
		#Change the frame rate according to application
		if cv2.waitKey(25) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()
