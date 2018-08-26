import cv2
import numpy as np
import time

current_position = 2250
firstFrame = None

cap = cv2.VideoCapture(1)

while True:
	stime = time.time()
	ret, frame = cap.read()

	if ret is False:
		print("Cam2 Error")

	frame = cv2.resize(frame, (800, 600))
	# cv2.line(frame, (0, 300), (800, 300), (0,0,255), 5)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (31, 31), 0)

	if firstFrame is None:
		firstFrame = gray
	else:
		firstFrame = preFrame

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=5)
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
	
	if contours:
		cnts = max(contours, key = lambda x: cv2.contourArea(x))

		m = cv2.moments(cnts)
		cx = int(m['m10']/m['m00'])
		cy = int(m['m01']/m['m00'])
		cv2.circle(frame, (0, cy), 6, (255,0,0), 10)
		cv2.circle(frame, (0, 20 * int(cy / 20)), 6, (0,255,0), 10)

		if cx <= 200:
			a = 1
		else:
			a = 0
		robot.write(str(a))

		move_steps = int(cy * 4500 / 600 - current_position)

# 		if (move_steps > 225) :
# 			quotient = int(move_steps / 225)
# 			print(quotient)
# 			move_steps1 = 225 * quotient
# #			print(move_steps1 + 4500)
# #			client.send(str(move_steps1 + 4500).encode())
# 			current_position = move_steps1 + current_position
# 		elif (move_steps < -225):
# 			quotient = int(move_steps / 225) + 1
# 			print(quotient)
# 			move_steps1 = 230 * quotient
# 			#print(move_steps1 + 4500)
# 			# client.send(str(move_steps1 + 4500).encode())
# 			current_position = move_steps1 + current_position

		if (move_steps > 225) or (move_steps < -225):
			quotient = int(move_steps / 225)
			#print(quotient)
			move_steps1 = 225 * quotient
			# print(move_steps1 + 4500)
			# client.send(str(move_steps1 + 4500).encode())
			current_position = move_steps1 + current_position
		
	key = cv2.waitKey(1)
	if key == 27:
		break

	preFrame = gray

	t_time = round(time.time() - stime, 3)
	t_text = str(t_time)
	cv2.putText(frame,t_text, (700, 45), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
	cv2.imshow("1", frame)

cap.release()
cv2.destroyAllWindows()
