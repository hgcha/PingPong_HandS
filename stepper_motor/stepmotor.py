
import socket
import wiringpi
import time

#HOST = "169.254.7.25"
HOST = "192.168.1.105"
PORT = 5050
BUFSIZE = 4
ADDR = (HOST, PORT)

server = socket.socket()
server.bind(ADDR)
server.listen(5)
client = None

OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0

ENABLE_PIN = 0
STEP = 2
DIR = 3

wiringpi.wiringPiSetup()
wiringpi.pinMode(ENABLE_PIN, OUTPUT)
wiringpi.pinMode(STEP, OUTPUT)
wiringpi.pinMode(DIR, OUTPUT)

wiringpi.digitalWrite(ENABLE_PIN, LOW)

while True:
	if client is None:
		print("waiting for connection...")
		client, addr_info = server.accept()
		print("got connection from", addr_info)
		wiringpi.digitalWrite(ENABLE_PIN, LOW)
	else:
#		client.send(b"hello")
		total_data = client.recv(BUFSIZE)
		total_data = total_data.decode()
#		if total_data :
#		print(int(total_data))
		print(total_data)
		total_data = int(total_data)
		total_data = total_data - 4500
#		total_data1 = total_data*(7.75)
#		print(total_data)
#		print(type(total_data))

		if total_data > 0:
			wiringpi.digitalWrite(DIR, HIGH)
			for i in range(0, total_data):
				wiringpi.digitalWrite(STEP, HIGH)
				time.sleep(0.0005)
				wiringpi.digitalWrite(STEP, LOW)
				time.sleep(0.0001)

		if total_data < 0:
			total_data = (-1) * total_data
			wiringpi.digitalWrite(DIR, LOW)
			for i in range(0, total_data):
				wiringpi.digitalWrite(STEP, HIGH)
				time.sleep(0.0005)
				wiringpi.digitalWrite(STEP, LOW)
				time.sleep(0.0001)

		time.sleep( 0.015 )
