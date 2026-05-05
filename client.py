import socket as sock
import time
s = sock.socket(sock.AF_INET,sock.SOCK_STREAM)
while True:
    try:
        s.connect(("localhost",8081))
        print("connect to the server")
        break
    except:
        print("can't connect to the server\n")

msg = "hello world hkhdkah akdhk dak ahll lalkh"
size = len(msg.encode("UTF-8"))
sendLen = 1028
totalSent = 0
s.sendall((str(size)+'\0').encode("UTF-8"))
time.sleep(1)
s.sendall((str(sendLen)+'\0').encode("UTF-8"))
time.sleep(1)
while totalSent < size:
    f = s.send(msg[totalSent:].encode("UTF-8"))
    if( f ==0):
        raise RuntimeError("Connection closed\n")
        continue
    totalSent += f
s.sendall(b'\0')

s.close()