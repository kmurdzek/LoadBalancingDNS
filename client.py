import socket
import threading
import argparse
def client(group_idx, idx):
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Group-{group_idx}, Client-{idx} socket created")
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())
    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)
    msg = "amazon.com"
    cs.send(msg.encode("utf-8"))
    data = cs.recv(200)
    print("Returned data: ", data.decode('utf-8'))
    print( "[C]: Group-{group_idx} Clien-{idx} received from server: {data.decode('utf-8')}")
    cs.close()
    exit()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
    "group_idx" , type=int, help="group idx of client groups"
    )
    args = parser.parse_args()
    thread_list = []
    for i in range(5):
        t = threading.Thread(
            name= "client-{i}", target=client, args=(args.group_idx, i)
        )
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    print("done.")