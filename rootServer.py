import select
import socket
from collections import defaultdict
def client(domainName):
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 50071   
    localhost_addr = socket.gethostbyname(socket.gethostname())
    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)
    cs.send(domainName)
    data = cs.recv(10)
    #data = data.decode('utf-8')
    #print("ip address ", data)
    cs.close()
    return data
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[S]: Sever socket created")
server.setblocking(0)
server_binding = ("", 50007)
server.bind(server_binding)
server.listen(10)

inputs = [server]
outputs = []
error = []
message_buffer = {}

while inputs:
    readable, writable, e = select.select(inputs, outputs, error, 30)
    if readable or writable:
        for r in readable:
            if r is server:
                conn, add = r.accept()
                conn.setblocking(0)
                inputs.append(conn)
            else:
                data = r.recv(100)
                print("[S]: server received: {data.decode('utf-8')}")
                outputs.append(r)
                message_buffer[r] = data
                inputs.remove(r)
        for w in writable:
            #this is just echoing the message from server
            #w is the actual socket we write too
            print("message associated with socket w:",  message_buffer[w])
            msg = message_buffer[w]
            data = client(msg.encode('utf-8')) #data from tns
            #lets query the dns server
            w.send(data) #this is what the client is receiving
            outputs.remove(w)
    else:
        print("[S]: time out, server exit")
        server.close()
        inputs.remove(server)


    
