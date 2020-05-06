from datetime import datetime
import socket

print('The client started at', datetime.now())

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b'Hello UDP', ('127.0.0.1', 50000))
client.close()