import socket

client = socket.socket()
HOST = "169.254.7.25"
PORT = 5003
BUFSIZE = 1024
ADDR = (HOST, PORT)

client.connect(ADDR)
print('Connected to', HOST)

while True:
    message = str(input("Enter something for the server: "))
    client.send(message.encode('utf-8'))