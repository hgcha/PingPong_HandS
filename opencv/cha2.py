import cv2
import numpy as np

x = []
y = []
G_avg = 0

cx = -1
cy = -1

firstFrame = None

cap = cv2.VideoCapture(0)
print(len(x))

while True:
	ret, frame = cap.read()

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

	if contours:
		cnts = max(contours, key = lambda x: cv2.contourArea(x))
		m = cv2.moments(cnts)
		((xloc, yloc), radius) = cv2.minEnclosingCircle(cnts)
		cv2.circle(frame, (int(xloc),int(yloc)), int(radius), (0, 255, 0), 10)

		if m['m00'] > 0:
			cx = (m['m10']/m['m00'])
			cy = (m['m01']/m['m00'])
			cv2.circle(frame, (int(cx), int(cy)), 1, (0, 255, 0), 10)
			x.append(cx)
			y.append(cy)

	if (3 <= len(x)) or (3 <= len(y)):

		x_compare = x[0] - x[1]
		if x_compare < 0:
			del x[:]
			del y[:]
			G_avg = 0
			cv2.imshow("1", frame);
			key = cv2.waitKey(1)
			if key == 27:
				break
			preFrame = gray
			continue

		G_avg = int( (((y[1] - y[0]) / (x[1] - x[0])) + ((y[2] - y[1]) / (x[1] - x[0]))) / 2 )
		x_final = 0
		y_final = G_avg * (x_final - x[0]) + y[0]

		cv2.line(frame, (int(x[0]), int(y[0])), (int(x_final), int(y_final)), (0,0,255), 10 )

		if (cx <= 10):
			del x[:]
			del y[:]
			G_avg = 0

	cv2.imshow("1", frame);

	key = cv2.waitKey(1)
	if key == 27:
		break

	preFrame = gray

cap.release()
cv2.destroyAllWindows()
