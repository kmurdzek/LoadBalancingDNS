#read in the tables
import select
import socket
import sys
from collections import defaultdict
dns = {}
with open("PROJ2-DNSTS2.txt", "r") as f:
    for line in f:
        delimed = line.split()
        dns[delimed[0]] = (delimed[1], delimed[2])
print(dns)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[S]: Sever socket created")
#server.setblocking(0)
server_binding = ("", int(sys.argv[1]))
server.bind(server_binding)
server.setblocking(0)
server.listen(10)


inputs = [server]
outputs = []
error = []
message_buffer = {}
client = None
while inputs:
    readable, writable, e = select.select(inputs, outputs, error, 30)
    if readable or writable:
        for r in readable:
            if r is server:
                conn, add = r.accept()
                client = conn
                conn.setblocking(0)
                inputs.append(conn) #adds the connection to the inputs that requested 
                #to access this socket, so the client
            else:
                #this runs when the readable is not the server but it is the socket
                #that we added to inputs the client
                #this gets initial message from the client
                data = r.recv(200)
                if(not data):
                        print("no data returned")
                        #reconnect the socket
                        inputs.remove(r)
                        continue
                if(r is client): #means were reading from client and preparing to send to client
                    if(client not in outputs):
                        outputs.append(client)           
                        message_buffer[client] = data
        for w in writable:
            if(w is client):
                print("writing to client : ", w)
                msg = message_buffer[client]
                print("MESSAGE", msg)
                if(dns.has_key(msg)):
                    ip = dns[msg]
                    print("Hello")
                    ip = ip[0] + " " + ip[1] + " IN"
                    w.send(ip.encode('utf-8'))
                    
                    print("sent back to rs :", ip)


            
            #once we send were going to want to add the socket to readable
            #because we will be expecting a response at the socket
                    
             #send data to the dns, 
            outputs.remove(w) #we dont want to write to that socket again so we 
            #remove it from where we still have to write to
    else:
        print("[S]: time out, server exit")
        server.close()
        inputs.remove(server)
        break
#checks the table for the domain
''''
print(data_from_rs.decode('utf-8'))
if(dns.has_key(data_from_rs.decode('utf-8'))):
    ip = dns[data_from_rs.decode('utf-8')]
    ip = ip[0] + " " + ip[1]
    csockid.send(ip.encode('utf-8'))
    print(ip)
server.close()
'''
