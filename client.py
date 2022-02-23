import socket
import threading
import argparse
import sys

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[C]: Group-{group_idx}, Client-{idx} socket created")
port = int(sys.argv[2])
localhost_addr = socket.gethostbyname(sys.argv[1])
print ("name of address:" + localhost_addr)
    # connect to the server on local machine
server_binding = (localhost_addr, port)
cs.connect(server_binding)


f = open("RESOLVED.txt", "w")
with open('PROJ2-HNS.txt') as textfile:
    for line in textfile:
        print(line)
        msg = line.strip()
        cs.send(msg.encode("utf-8"))
        data = cs.recv(200)
        print("Returned data: ", data.decode('utf-8'))
        f.write (msg + " " + data.decode('utf-8') + "\n")

f.close()
cs.close()
exit()
