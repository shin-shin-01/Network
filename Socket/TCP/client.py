from datetime import datetime
import socket

print('The client started at', datetime.now())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 50000))
    s.sendall(b'Hello TCP')
    
    data = s.recv(1024) ## Receive
    print(repr(data))