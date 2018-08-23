import cv2
import numpy as np
import socket
import time
import serial

client = socket.socket()
#HOST = "169.254.7.25"
HOST = "192.168.1.105"
PORT = 5052
BUFSIZE = 4
ADDR = (HOST, PORT)

client.connect(ADDR)
print('Connected to', HOST)

robot = serial.Serial("/dev/ttyUSB1", 9600)

current_position = 2325
firstFrame = None

cap = cv2.VideoCapture(0)

while True:
	stime = time.time()
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
	
	if contours:
		cnts = max(contours, key = lambda x: cv2.contourArea(x))

		m = cv2.moments(cnts)
		cx = int(m['m10']/m['m00'])
		cy = int(m['m01']/m['m00'])
		print(cy)
		cv2.circle(frame, (0, cy), 6, (0,0,255), 10)

		# send_x = int( cx/10 )
		if cx in range(10, 50):
			robot.write(b'1')
		else :
			robot.write(b'0')
		# robot.write()

		move_steps = int(cy * (4650/600) - current_position)
		current_position = current_position + (move_steps)
		# if current_position < 0:
		# 	current_position = 0
		# elif current_position > 4650:
		# 	current_position = 4650
		move_steps = move_steps + 4650
		client.send(str(move_steps).encode())

	key = cv2.waitKey(1)
	if key == 27:
		break

	preFrame = gray

	t_time = round(time.time() - stime, 3)
	t_text = str(t_time)
	cv2.putText(frame,t_text, (700, 45), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
	cv2.imshow("1", frame)

cap.release()
cv2.destroyAllWindows()
