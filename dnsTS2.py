#read in the tables
import socket
dns = {}
with open("PROJ2-DNSTS2.txt", "r") as f:
    for line in f:
        delimed = line.split()
        dns[delimed[0]] = (delimed[1], delimed[2])
print(dns)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[S]: Sever socket created")
#server.setblocking(0)
server_binding = ("", 50072)
server.bind(server_binding)
server.listen(10)
csockid, addr = server.accept()
data_from_rs = csockid.recv(200)
#checks the table for the domain
print(data_from_rs.decode('utf-8'))
if(dns.has_key(data_from_rs.decode('utf-8'))):
    ip = dns[data_from_rs.decode('utf-8')]
    ip = ip[0] + " " + ip[1]
    csockid.send(ip.encode('utf-8'))
    print(ip)
else:
    #ip = "0.0.0.0"
    #csockid.send(ip.encode('utf-8'))
    pass
server.close()