import cv2
import numpy as np
import random 
from clusterMeanShift import cluster
#To display the target video
stat_array = []
car_in = False # to check if the car is actively being tracked or not 
vehicle_count = 0 
def play_video(video_file,sleepTime,x1,y1,x2,y2,trim_begin,trim_end,display_window_name):
	
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
def count_cars(video_file,sleepTime,x1,y1,x2,y2,trim_begin,trim_end,display_window_name):
	global stat_array # keeps track of the positions where car crosses the line ::: Logic variable 
	global vehicle_count
	global car_in


	target_row =  600
	cv2.namedWindow(display_window_name)
	cap = cv2.VideoCapture(video_file)
	reference_frame = None
	image_area = None

	ret, ref_frame = cap.read()
	#ref_frame = ref_frame[:,500:1100,:]
	image_area = ref_frame.shape[0] * ref_frame.shape[1]

	while(cap.isOpened()):
		#reading frame by frame
		ret, frame = cap.read()

		if ret is False:
			print vehicle_count
			exit()

		#frame = frame[:,500:1100,:]
		frame = np.array(frame,dtype='uint8')
		#frame = cv2.line(frame,(100,650),(600,600),(255,0,255),5)
		frame = cv2.line(frame,(100,300),(300,300),(0,0,255),1)
		#frame = cv2.line(frame,(100,550),(600,550),(0,0,255),1)
		
		#Count-Vehicles Test
		cv2.putText(frame, "Cars : {}".format(vehicle_count), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0,255), 2)
		

		#Getting the reference frame
		if ret is not None and reference_frame is None:
			reference_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			reference_frame = cv2.GaussianBlur(reference_frame,(29,29),0)
			image_area = frame.shape[0] * frame.shape[1]
			continue
	
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		#blurring each frame :: to aid in contour detection
		blurred = cv2.GaussianBlur(gray,(29,29),0)

		#finding the difference in frames
		delta = cv2.absdiff(reference_frame, blurred)
		
		ret1, thresh = cv2.threshold(delta,30,255,cv2.THRESH_BINARY)
		#dilate is done to close the small holes in the image
		thresh = cv2.dilate(thresh, None, iterations=5)
		#cv2.imshow("Thresholded",thresh)
		#cv2.waitKey(0)
		
		

		'''
		fgmask = fgbg.apply(frame)
		ff = cv2.medianBlur(fgmask,7)
		ret1, thresh = cv2.threshold(ff,128,255,cv2.THRESH_BINARY)


		cv2.imshow("Thresholded",thresh)
		#cv2.waitKey(0)
		'''

		#Detecting contours

		(_,cnt,_) = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
		for contour in cnt:
			#need to find a suitable area range to filter the contours
			contour_area = cv2.contourArea(contour)
			if (contour_area >0.009 * image_area) and  (contour_area <0.10* image_area):
				

				### Moments are required to calculate the center point ###
				#M = cv2.moments(contour)
				#cX = int(M["m10"] / M["m00"])
				#cY = int(M["m01"] / M["m00"])
				#cv2.circle(frame, (cX, cY), 1, (255,111,251), 1)
				### The center point will be used to count the cars #######
				(x,y,w,h) = cv2.boundingRect(contour)
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
				cv2.line(frame,(x+w/2,y),(x+w/2,y+h),(255,0,0),3)



				#cv2.drawContours(frame,cnt,-1,(0,255,0),3)
				cv2.imshow(display_window_name,frame)

				#### Include the logic of line crossing ###########	
				#### Logic 1 : Count the number of Color dots crossing the line [Does Not Work]
				#### Logic 2 : Use Random color lines and count the number of unique lines. When car not passing refresh array [Does not work]
				#### Logic 3 : Statistics approach [Works :: Needs Tweaks]

				
				line_check_array = frame[200,100:200,0] #The RED line color marker (0,0,255) 
				# The Blue component of the line should be blue in color 
				#print line_check_array

				for i in range(len(line_check_array)):
					if line_check_array[i] != 0: 
						car_in = True
						## It toched the line 
						## Keep counting and inserting the array from now
						## 
						stat_array.append(i+100)
						
					else:
						continue 
				
				if car_in == True :
					# means that in this frame the car was being tracked
					# change the state to false
					car_in=False
				else:
					#car_in was false :: meaning that the car was abset in this frame 
					#this is where i will compute the threshold stats and sed it for clustering

					#find range = max-min from the cluster .... to get the range
					if len(stat_array) > 0:
						#case when video starts and no cars are still at the line and array contains nothing
						diff = max(stat_array) - min(stat_array)
						if (diff <80):
							#means that only one vehicle was present
							vehicle_count = vehicle_count + 1 
						else:
							#since vehicles are more than 1 send for clustering
							clusters = cluster(stat_array)
							vehicle_count = vehicle_count + clusters
						#cleaning the array for further analysis
						del stat_array[:]


		#Video stops playing if 'q' or escapse is pressed
		#Change the frame rate according to application
		if cv2.waitKey(sleepTime) == ord('q'):
			print vehicle_count
			break
	
	cap.release()
	cv2.destroyAllWindows()
