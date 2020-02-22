import picamera
import time
import cv2
import numpy as np
import motor_driver

from picamera.array import PiRGBArray

RoadCenter=[0,0]
LastRoadCenter = [0,0]

if __name__ == "__main__":
	RaspCar = motor_driver.CarControler()

	with picamera.PiCamera() as camera:
#open camera
		camera.resolution = (160,120)
		camera.framerate  = 30
		RawCapture = PiRGBArray(camera,size=(160,120))
		time.sleep(2)
#		camera.capture("test12.jpg")

		for frame in camera.capture_continuous(RawCapture,format="bgr",use_video_port=True):
			ImageRaw = frame.array
#			ImageRaw = cv2.imread("./test12.jpg")
			ImageCut = ImageRaw[90-1:120-1][1-1:160-1]	
			ImageGray = cv2.cvtColor(ImageCut,cv2.COLOR_BGR2GRAY)
			cv2.imshow("ImageGray",ImageGray)	#gray image of camera	
		
			ret,ImageBinary = cv2.threshold(ImageGray,165,255,cv2.THRESH_BINARY)#150
#			cv2.imshow("ImageBinary",ImageBinary)

			kernel = np.ones((3,3),np.uint8)
			ImageCC = cv2.morphologyEx(ImageBinary,cv2.MORPH_CLOSE,kernel)
			cv2.imshow("ImageBinary",ImageCC)
			(contours,_) = cv2.findContours(ImageCC,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
			try:
				Area = []
				CarLine = []
				Len = 0						
				ImageFindPoint = ImageBinary
				for i in range(len(contours)):
					Area.append(cv2.contourArea(contours[i]))
				Index_max = np.argmax(Area)	#if not found, go to ValueError
#				print Area[Index_max]
				if(Area[Index_max]<150):
					print("found failed")
				else:
					cv2.fillConvexPoly(ImageFindPoint,contours[Index_max],125)			
					
					FlagTurnRight = 1
					FlagTurnLeft  = 1
					FlagReachBottom = 0
					for i in list(reversed(range(len(ImageFindPoint)))):
						for j in range(len(ImageFindPoint[0])):
							if ImageFindPoint[i][j] == 125:
								CarLine.append([i,j])
								if len(ImageFindPoint)- i <3 :
									FlagReachBottom = 1				#bottom detct
									cv2.fillConvexPoly(ImageCut,contours[Index_max],[255,255,0])

						if CarLine and FlagReachBottom:  			#list is not empty
							Len = len(CarLine)
							RightLineLack = len(ImageGray[0]) - CarLine[Len-1][1]  < 3
							LeftLineLack = CarLine[0][1] < 2

							if RightLineLack and LeftLineLack:
								RoadCenter[0] = len(ImageFindPoint)
								RoadCenter[1] = len(ImageFindPoint[0])/2	
						
								CarLine = []		
							elif RightLineLack and not LeftLineLack:	#detect only left carline
								if FlagTurnRight :
									RoadCenter[0] = CarLine[0][0]
									RoadCenter[1] = CarLine[0][1]+90

								FlagTurnRight = 0
								CarLine = []
							elif LeftLineLack and not RightLineLack:	#detect only right carline
								if FlagTurnLeft :
									RoadCenter[0] = CarLine[0][0]
									RoadCenter[1] = CarLine[Len-1][1]-90
								
								FlagTurnLeft  = 0
								CarLine = []
							else:
#								print CarLine[Len-1][1]-CarLine[0][1]
								if CarLine[Len-1][1]-CarLine[0][1]<20:
									CarLine = []
								else:	
									RoadCenter[0] = CarLine[0][0]
									RoadCenter[1] = (CarLine[0][1]+CarLine[Len-1][1])/2
								break;

				if Len == 0:			#not found carline
					RoadCenter[0] = LastRoadCenter[0]
					RoadCenter[1] = LastRoadCenter[1]

			except ValueError :
				print ("ValueError")
				RoadCenter[0] = LastRoadCenter[0]
				RoadCenter[1] = LastRoadCenter[1]

			finally:	
				LastRoadCenter[0] = RoadCenter[0]
				LastRoadCenter[1] = RoadCenter[1]

				cv2.circle(ImageCut,tuple(reversed(RoadCenter)),5,(0,0,255),-1)
				cv2.imshow("ImageFindPoint",ImageCut)
#car control part:
				Error = len(ImageGray[0])/2-RoadCenter[1]
				print "RoadCenter:",RoadCenter,"	Error:",Error
				RaspCar.autorun(Error)

				RawCapture.truncate(0)				#clear the stream
				if cv2.waitKey(1) == 27:			#update:1ms
					break





