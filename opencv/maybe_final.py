import cv2
import numpy as np
import socket
import time
import serial
import threading
locka = threading.Lock() 
a = 1 

client = socket.socket()
#HOST = "169.254.7.25"
HOST = "192.168.1.105"
PORT = 5051
BUFSIZE = 4
ADDR = (HOST, PORT)

client.connect(ADDR)
print('Connected to', HOST)

robot = serial.Serial("/dev/ttyACM0", 9600)

cap = cv2.VideoCapture(1)
cap1 = cv2.VideoCapture(0)

def cha2():
	global client
	global cap
	global a
	global locka

	z_ref = [0, 0, -100, -220, -520, -670, -820]

	current_position = 2250
	firstFrame = None

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
				locka.acquire()         
				a = 1
				locka.release()
			locka.acquire()
			robot.write(str(a))
			locka.release()

			move_steps = int(cy * 4500 / 600 - current_position)

			if (move_steps > 300):
				quotient = int(move_steps / 300)
				move_steps1 = 300 * quotient
#				print(move_steps1 + 4500)
				move_steps1 = move_steps1 - z_ref[a] 
				client.send(str(move_steps1 + 4500).encode())
				current_position = move_steps1 + current_position
			elif (move_steps < -300):
				quotient = int(move_steps / 300) + 1
				move_steps1 = 300 * quotient
#				print(move_steps1 + 4500)
				move_steps1 = move_steps1 - z_ref[a] 
				client.send(str(move_steps1 + 4500).encode())
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

def cha3():
	global cap1
	global robot
	global a
	global locka
	while True:
		stime1 = time.time()
		ret1, frame1 = cap1.read()
		rows, cols = frame1.shape[:2]

		if ret1 is False:
			print("Cam1 Error")

		frame1 = cv2.resize(frame1, (800, 500))
		M = cv2.getRotationMatrix2D((cols / 2, rows / 2),  90, 1)
		frame1 = cv2.warpAffine(frame1, M,(cols, rows))
		frame1 = frame1[0:350, 300: 500]
		hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
		orange = cv2.inRange(hsv, np.array([10, 90, 50]), np.array([20, 255, 255]))
		contours1 = cv2.findContours(orange.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
		
		if contours1:
			cnts1 = max(contours1, key = lambda x: cv2.contourArea(x))
			m1 = cv2.moments(cnts1)
			if m1['m00'] > 0:
				cx1 = int(m1['m10']/m1['m00'])
				cz = int(m1['m01']/m1['m00'])
				cv2.circle(frame1, (cx1, cz), 7, (0,0,255), 10)
				cv2.circle(frame1, (0, cz), 6, (255,0,0), 10)

				locka.acquire()
				a = int(cz / 70) + 2
				robot.write(str(a))
				locka.release()
				#print(send_z)
				# print(robot.read(1))

		key1 = cv2.waitKey(1)
		if key1 == 27:
			break

		t_time1 = round(time.time() - stime1, 3)
		t_text1 = str(t_time1)
		cv2.putText(frame1,t_text1, (300, 45), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
		cv2.imshow("2", frame1)

	cap1.release()
	cv2.destroyAllWindows()


fir = threading.Thread(target = cha2,)
fir.start()
sec = threading.Thread(target = cha3,)
sec.start()
