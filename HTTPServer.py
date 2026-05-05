import socket
import os

def makeSocket():
    global sock
    sock = socket.socket()
    sock.bind(("localhost",8080))
    sock.listen(5)
def connection()->tuple[socket.socket,socket._Address]:
    return sock.accept()
def sendContinous(msg:str,s2:socket.socket):
    msg_encoded = msg.encode("UTF-8")
    msg_len = len(msg_encoded)
    toal_send = 0
    while toal_send < msg_len:
        s = s2.send(msg_encoded[toal_send:])
        if s == 0:
            assert RuntimeError("connection closed")
        toal_send += s
def sendALL(msg:str,s2:socket.socket):
    msg_encoded = msg.encode("UTF-8")
    a = s2.sendall(msg_encoded)
    if a == None:
        assert RuntimeError("connection lost")

def recive(s2:socket.socket)->bytes:
    return s2.recv(1024)
def reciveHeader(s2:socket.socket)->str:
    msg = ''
    while True:
        a = recive(s2).decode("UTF-8")
        msg+=a
        if("\r\n\r\n" in a ):
            return msg
            break
    return msg

html = """
            <html>
            <body>
                <h1>Coustom home server</h1>
            </body>
            </html>
            """
msg = """HTTP/1.1 200 OK\nDate: Tue, 05 May 2026 12:00:00 GMT\nServer: custom HTTP Server\nContent-Type: text/html; charset=UTF-8\nContent-Length: {}\nConnection: close

            {}
        """
Message =  msg.format(len(html),html)
Error =  """
        <html>
        <h1>404 NotFound</h1>
        </html>
"""
Error_Message = msg.format(len(Error),Error)
def HeaderProcessing(header:str):
    global Message,msg
    i = 3
    j = header.index("HTTP")
    Resource = header[i:j]
    if(Resource == " / "):
        html = ''
        with open("backend/HTML/home.html","r") as file:
            html = file.read()
        print(html)
        Message = msg.format(len(html),html)
        return None
    else:
        try :
            html = ''
            with open("backend/HTML/{}".format(Resource[1:-1]+".html"),"r") as file:
                html = file.read()
            print(html)
            Message = msg.format(len(html),html)
            return None
        except:
            Message = Error_Message

try :
    makeSocket()
    c1 = connection()

    while(True):
        data = reciveHeader(c1[0])
        print(data,'\n')
        HeaderProcessing(data)
        sendContinous(Message,c1[0])
        c1[0].close()
        c1 = connection()
except KeyboardInterrupt:
    sock.close()
    exit()