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

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()


	if ret is False:
		print("Cam Error")

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (11, 11), 0)

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
		((x, y), radius) = cv2.minEnclosingCircle(cnts)

		if m['m00'] > 0:
			cx = int(m['m10']/m['m00'])
			cy = int(m['m01']/m['m00'])

			center = (cx, cy)

			if radius > 10:
				cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,0), 2)
				cv2.circle(frame, center, 5, (0, 255, 0), -1)

		pts.appendleft(center)
		print(center)

		for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
			if pts[i - 1] is None or pts[i] is None:
				continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	cv2.imshow("1", frame)
	key = cv2.waitKey(1)
	if key == 27:
		break

	preFrame = gray

cap.release()
cv2.destroyAllWindows()
