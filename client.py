import socket
import threading
import argparse

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[C]: Group-{group_idx}, Client-{idx} socket created")
port = 50007
localhost_addr = socket.gethostbyname(socket.gethostname())
    # connect to the server on local machine
server_binding = (localhost_addr, port)
cs.connect(server_binding)
msg = "GOOGLE.com"
cs.send(msg.encode("utf-8"))
data = cs.recv(200)
print("Returned data: ", data.decode('utf-8'))
print( "[C]: Group-{group_idx} Clien-{idx} received from server: {data.decode('utf-8')}")
cs.close()
exit()
