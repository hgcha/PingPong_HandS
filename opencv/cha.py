import cv2
import numpy as np
import argparse
from collections import deque

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())
pts = deque(maxlen=args["buffer"])

firstFrame = None

x = [] * 5
y = [] * 5
G = [] * 4
i = 0
G_total = 0
G_avg = 0

x_final = -1
y_final = -1

cap = cv2.VideoCapture(0)

rows = 600
cols = 800

while True:
	ret, frame = cap.read()

	if ret is False:
		print("Cam Error")
	frame = cv2.resize(frame, (800, 600))
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

			if radius > 10:
				cv2.circle(frame, (int(xloc), int(yloc)), int(radius), (0,255,0), 2)
				cv2.circle(frame, (int(cx),int(cy)), 5, (0, 255, 0), -1)

			if i < 3:
				x.append(cx)
				y.append(cy)

			elif i == 3 :
				if x[0] > x[1] :
					for t in range(0, 2):
						G.append(int( (y[t+1] - y[t]) / (x[t+1] - x[t]) ))

					for f in range(0, 2):
						G_total += G[f]

					G_avg = int(G_total / 4)

					if G_avg < 0:				#down
						G_compare = int( (rows - y[0]) / (0 - x[0]))
						if G_compare > G_avg:	#height = frame.rows - y[0]
							x_final = ( 1 / G_avg ) * (rows - y[0]) + x[0]
							y_final = rows
						elif G_compare < G_avg:	#weight = frame.cols
							x_final = 0
							y_final = (G_avg) * ( 0 - x[0] ) + y[0]
						else:
							x_final = 0
							y_final = rows
					elif G_avg > 0:				#up
						G_compare = int( (rows - y[0]) / (0 - x[0]))
						if G_compare > G_avg:	#weight = frame.rows - y[0]
							x_final = 0
							y_final = ( G_avg ) * ( 0 - x[0] ) + y[0]
						elif G_compare < G_avg:	#height = y[0]
							x_final = ( 1 / G_avg ) * (0 - y[0]) + x[0]
							y_final = 0
						else:
							x_final = 0
							y_final = 0
					else:
						x_final = 0
						y_final = y[0]

					cv2.line(frame, (int(x[0]), int(y[0])), (int(x_final), int(y_final)), (0,0,255), 10 )
					print(x_final)
					print(y_final)
					print("===============")

				else:
					del x[:]
					del y[:]
					del G[:]
					i = -1
					G_avg = 0
					G_compare = 0
					G_total = 0	

			elif i > 3:
				if cx <= 30:
					del x[:]
					del y[:]
					del G[:]
					i = -1
					G_avg = 0
					G_compare = 0
					G_total = 0	
				else:
					pass

			i = i + 1

	cv2.imshow("1", frame)
	key = cv2.waitKey(1)
	if key == 27:
		break

	preFrame = gray

cap.release()
cv2.destroyAllWindows()
