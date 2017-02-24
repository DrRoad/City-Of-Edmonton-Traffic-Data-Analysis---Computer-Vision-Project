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


#This function will count the total number of cars in the video
def count_cars(video_file,sleepTime,display_window_name):
	
	cv2.namedWindow(display_window_name)
	cap = cv2.VideoCapture(video_file)
	reference_frame = None
	image_area = None

	while(cap.isOpened()):
		#reading frame by frame
		ret, frame = cap.read()

		if ret is not None and reference_frame is None:
			reference_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			reference_frame = cv2.GaussianBlur(reference_frame,(29,29),0)
			image_area = frame.shape[0] * frame.shape[1]
			continue


		#trying otsu thresholding
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray,(29,29),0)

		#finding the difference in frames
		delta = cv2.absdiff(reference_frame, blurred)


		#blurring each frame :: to aid in contour detection
		
		ret1, thresh = cv2.threshold(delta,20,255,cv2.THRESH_BINARY)
		thresh = cv2.dilate(thresh, None, iterations=2)
		cv2.imshow("Thresholded",thresh)
		#cv2.waitKey(0)




		#Detecting contours
		(_,cnt,_) = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		for contour in cnt:
			#need to find a suitable area range to filter the contours
			contour_area = cv2.contourArea(contour)
			if (contour_area >0.001 * image_area) and  (contour_area <0.2 * image_area):

				(x,y,w,h) = cv2.boundingRect(contour)
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)


				#cv2.drawContours(frame,cnt,-1,(0,255,0),3)
				cv2.imshow(display_window_name,frame)




		#Video stops playing if 'q' or escapse is pressed
		#Change the frame rate according to application
		if cv2.waitKey(25) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()
