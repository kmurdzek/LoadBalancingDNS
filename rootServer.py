import select
import socket
from collections import defaultdict

cs1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port1 = 50071   
localhost_addr1 = socket.gethostbyname(socket.gethostname())
# connect to the server on local machine
server_binding1 = (localhost_addr1, port1)
cs1.connect(server_binding1)

cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port2 = 50072   
localhost_addr2 = socket.gethostbyname(socket.gethostname())
# connect to the server on local machine
server_binding2 = (localhost_addr2, port2)
cs2.connect(server_binding2)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[S]: Sever socket created")
server.setblocking(0)
server_binding = ("", 50007)
server.bind(server_binding)
server.listen(10)

inputs = [server,cs1, cs2] #where we read from
outputs = [] #where we send to 
error = []
message_buffer = {} #stores the messages
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
                
                if(r is cs1 or r is cs2): #means were reading from dns and preparing to send to client
                    if(client not in outputs):
                        outputs.append(client)
                        message_buffer[client] = data
                    print(data, "stalled before here1")
                    print("DNS Socket: ", cs1, " message from dns1 to client : ", message_buffer[client])
                if(r is client): #message we received from client and preparing for dns
                    outputs.append(cs1)
                    outputs.append(cs2)
                    message_buffer[cs1] = data
                    message_buffer[cs2] = data
                    print("Client Socket: ", client, " message from client to dns : ", message_buffer[cs1])
                inputs.remove(r)
        for w in writable:
            
            if(w is cs1):
                print("writing to dns1 : ", w)
                msg = message_buffer[cs1]
                w.send(msg.encode('utf-8'))
            if(w is cs2):
                print("writing to dns2 : ", w)
                msg = message_buffer[cs2]
                w.send(msg.encode('utf-8'))
            if(w is client):
                print("writing to client : ", w)
                msg = message_buffer[client]
                if(message_buffer[client] is ''):
                    msg = "DomainName - TIMED OUT"
                w.send(msg.encode('utf-8'))

            
            #once we send were going to want to add the socket to readable
            #because we will be expecting a response at the socket
                    
             #send data to the dns, 
            outputs.remove(w) #we dont want to write to that socket again so we 
            #remove it from where we still have to write to
    else:
        print("[S]: time out, server exit")
        server.close()
        cs1.close()
        cs2.close()
        inputs.remove(server)


    
