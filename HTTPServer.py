import socket
import os

html = """
            <html>
            <body>
                <h1>Coustom home server</h1>
            </body>
            </html>
            """
msg = """HTTP/1.1 200 OK\nDate: Tue, 05 May 2026 12:00:00 GMT\nServer: custom HTTP Server\nContent-Type: text/{}; charset=UTF-8\nContent-Length: {}\nConnection: close\r\n\r\n{}
        """
Message =  msg.format("html",len(html),html)
Error =  """
        <html>
        <h1>404 NotFound</h1>
        </html>
"""
Error_Message = msg.format("html",len(Error),Error)
image_formate_supported = [".png",".jpg"]

def makeSocket():
    global sock
    sock = socket.socket()
    sock.bind(("localhost",8081))
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
def sendContinousNoEncoding(msg:bytes,s2:socket.socket):
    msg_len = len(msg)
    toal_send = 0
    while toal_send < msg_len:
        s = s2.send(msg[toal_send:])
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

def reciveHttpMessage(s2:socket.socket)->list[str]:
    msg = ''
    Message_Length = 0
    Message_read = 0
    while Message_Length >= Message_read:
        a = recive(s2).decode("UTF-8")
        msg +=a
        if("\r\n\r\n" in msg):
            i = msg.find("Content-Length:")
            if(i == -1):
                return [msg,"\0"]
            i += 15
            j = msg.find("\n",i)
            Message_Length = int(msg[i:j])
            Message_read = len(msg)-(msg.find("\r\n\r\n")+4)
        if Message_Length != 0:
            Message_read +=len(a)
    return msg.split("\r\n\r\n")

def POST(data:str):
    pass

def GET(resource:str):
    global Message,msg
    try:
        extension = resource[resource.index("."):]
        print(extension)
        if(extension == ".html"):
            try :
                html = ''
                with open("HTML{}".format(resource),"r") as file:
                    html = file.read()
                print(html)
                Message = msg.format("html",len(html),html)
                return None
            except:
                Message = Error_Message
        if(extension == ".css"):
            try :
                css = ''
                with open("CSS{}".format(resource),"r") as file:
                    css = file.read()
                print(css)
                Message = msg.format(len(css.encode("UTF-8")),css)
                return None
            except:
                Message = Error_Message
        if(extension in image_formate_supported):
            try :
                img = ''
                with open("IMG{}".format(resource),"br") as file:
                    img = file.read()
                Message = msg.format("image/{}".format(extension[1:]),len(img),img)
                return None
            except:
                Message = Error_Message
        Message = Error_Message
    except:
        Message = Error_Message

def HeaderProcessing(header:str):
    global Message,msg
    i = 0
    j = 3
    opernation = header[i:j]
    if(opernation == "GET"):
        GET(header[4:header.index("HTTP")].strip())
        return None
    Message = Error_Message


def HttpMessageProcessing(Message:list[str]):
    HeaderProcessing(Message[0])
    print("Header\n",Message[0])
    print("Message",Message[1])



c1:tuple[socket.socket,socket._Address]
try :
    makeSocket()
    c1 = connection()

    while(True):
        # data = reciveHeader(c1[0])
        # print(data,'\n')
        # HeaderProcessing(data)
        message  =reciveHttpMessage(c1[0])
        HttpMessageProcessing(message)
        sendContinous(Message,c1[0])
        c1[0].close()
        c1 = connection()
except KeyboardInterrupt:
    sock.close()
    c1[0].close()
    exit()