import cv2
import numpy as np
import threading
import logging

x = []
y = []
count = 0

rows = 300
cols = 400

firstFrame = None

def camera1():
	cap = cv2.VideoCapture(1)
	ret, frame = cap.read()

	if ret is False:
		logging.error("Cam1 is Error")

	return frame

#def camera2():
#	cap1 = cv2.VideoCapture(2)
#	ret1, frame1 = cap1.read()

#	if ret1 is False:
#		print("Cam2 is Error")

#	return frame

def imageProcessing(frame_):
	frame = cv2.resize(frame_, (800, 600))
	gray = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (31, 31), 0)

	if firstFrame is None:
		firstFrame = gray
	else:
		firstFrame = preFrame

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

	if not contours:
		pass
	else:
		cnts = max(contours, key = lambda x: cv2.contourArea(x))
		m = cv2.moments(cnts)
		((xloc, yloc), radius) = cv2.minEnclosingCircle(cnts)

		if m['m00'] > 0:
			cx = (m['m10']/m['m00'])
			cy = (m['m01']/m['m00'])

			center = (cx, cy)

			if radius > 5:
				cv2.circle(frame_, (int(xloc), int(yloc)), int(radius), (0,255,0), 2)
				cv2.circle(frame_, (int(cx),int(cy)), 5, (0, 255, 0), -1)

	cv2.imshow("1", frame_)

	if cx and cy is True:
		return cx, cy, gray
	else:
		return -1, -1, gray


def prediction(c_x, c_y):
	count = count + 1

	x.append(c_x)
	y.append(c_y)

	if count >= 2:
		if x[0] < x[1]:
			del x[:]
			del y[:]
			count = 0
			G_avg = 0
			G_total = 0
			G_compare = 0
		elif x[0] >= x[1]:
			if x[2] is True:
				if G_avg is False:
					for t in range(0, 2):
						G_total += int( (y[t+1] - y[t]) / (x[t+1] - x[t]) )

					G_avg = int(G_total / 3)
					G_compare = int( (rows - y[0]) / (0 - x[0]))

					if G_avg < 0:				#down
						if G_compare < G_avg:	#weight = frame.cols
							x_final = 0
							y_final = (G_avg) * ( 0 - x[0] ) + y[0]
						else:
							x_final = 0
							y_final = rows
					elif G_avg > 0:				#up
						if G_compare > G_avg:	#weight = frame.rows - y[0]
							x_final = 0
							y_final = ( G_avg ) * ( 0 - x[0] ) + y[0]
						else:
							x_final = 0
							y_final = 0
					else:
						x_final = 0
						y_final = y[0]
					return y_final
				else:
					if c_x <= 25:
						del x[:]
						del y[:]
						count = 0
						G_avg = 0
						G_total = 0
						G_compare = 0



def main():

	img1 = threading.Thread()
