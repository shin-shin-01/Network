from datetime import datetime
import socket

print('The server started at', datetime.now())
print('Waiting...')

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
## DYNAMIC AND/OR PRIVATE PORTS 50000
server.bind(('127.0.0.1', 50000))

data, addr = server.recvfrom(1024)
print('at', datetime.now(), 'data: ', data, 'addr: ', addr)
server.close()