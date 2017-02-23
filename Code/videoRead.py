import cv2

video_file = '../Dataset/StAlbert/traffic_south.MP4'
cap = cv2.VideoCapture(video_file)

cv2.namedWindow("Target Video")
while(cap.isOpened()):
	#reading frame by frame
	ret, frame = cap.read()

	cv2.imshow("Target Video",frame)

	#Video stops playing if 'q' or escapse is pressed
	#Change the frame rate according to application
	if cv2.waitKey(25) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()