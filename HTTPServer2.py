"""Copyright (C) 2026  Ayush Mishra"""


import socket 
import os
import threading 
from urllib.parse import parse_qs
import json

global image_formate_supported
image_formate_supported = (".jpg",".png") #read only writing forbidden 
msg = """HTTP/1.1 200 OK\nDate: Tue, 05 May 2026 12:00:00 GMT\nServer: custom HTTP Server\nContent-Type: {}; charset=UTF-8\nContent-Length: {}\nConnection: close\r\n\r\n"""

class HTTPSocket():
    def __init__(self,sock:socket.socket,id :int,msg_formate:str):
        self.sock:socket.socket = sock
        self.id = id
        self.alive = True
        self.recive = ''
        self.send = ''
        self.formate = msg_formate
        self.HTTPpipeline()
    def SendData(self,msg:bytes,msg_len:int):
        sended = 0
        while sended < msg_len:
            s = self.sock.send(msg[sended:])
            if(s == 0):
                return -1
            sended += s
    def ReciveData(self):
        message_length = 0
        messaged_recived = 0
        while message_length >=messaged_recived:
            a = self.sock.recv(4096).decode("UTF-8")
            self.recive += a # type: ignore
            if "\r\n\r\n" in a :
                i = self.recive.find("Content-Length:") #type:ignore
                if( i  == -1):
                    self.recive = (self.recive,None)
                    return None
                i += 15 #to go to where the value is located
                j = self.recive.index("\n",i)
                message_length = int(self.recive[i:j])#type:ignore
                messaged_recived = len(self.recive) - self.recive.index("\r\n\r\n")+4
            if(message_length != 0):
                messaged_recived += len(a)
        self.recive = self.recive.split("\r\n\r\n")
    def  HTTPprocessing(self):
            i = 0
            j = 4
            opernation = self.recive[0][i:j].strip()
            print(opernation)
            if(opernation == "GET"):
                return self.GET(self.recive[0][4:self.recive[0].index("HTTP")].strip())
            if(opernation == "POST"):
                i = self.recive[0].index("Content-Type:")
                i += 13
                j = self.recive[0].index("\n",i)
                return self.POST(self.recive[1],self.recive[0][i:j].strip()) #type:ignore
            message = "Method Not supported".encode("UTF-8")
            return ("text/html",len(message),message)

    def GET(self,resource:str)->tuple[str,int,bytes]:
        try:
            extension = resource[resource.index("."):]

            if(extension == ".html"):
                try :
                    html = ''
                    with open("HTML{}".format(resource),"r") as file:
                        html = file.read()
                    html = html.encode("UTF-8")
                    return ("text/html",len(html),html)
                except:
                    Message = "404 File Not Found".encode("UTF-8")
                    return ("text/html",len(Message),Message)
                

            if(extension == ".css"):
                try :
                    css = ''
                    with open("CSS{}".format(resource),"r") as file:
                        css = file.read()
                    css = css.encode("UTF-8") 
                    return ("text/css",len(css),css)
                except:
                    Message = "404 File Not Found".encode("UTF-8")
                    return ("text/html",len(Message),Message)
                

            if(extension in image_formate_supported):
                try :
                    img = ''
                    with open("IMG{}".format(resource),"br") as file:
                        img = file.read()
                    return ("image/{}".format(extension[1:]),len(img),img)
                except:
                    Message = "404 File Not Found".encode("UTF-8")
                    return ("text/html",len(Message),Message)
            Message = "404 File Not Supported".encode("UTF-8")
            return ("text/html",len(Message),Message)
        except:
            Message = "405 Request Not Supported".encode("UTF-8")
            return ("text/html",len(Message),Message)
    
    def POST(self,Request:str,type:str):
        try:
            with open("test.txt","+a") as file:
                if type == "application/x-www-form-urlencoded":
                    data = json.dumps(parse_qs(Request),indent=4)
                    file.write(data)
                    return (" ",0,b"\0")
                Message = "Data type Not Supported".encode("UTF-8")
                return ("text/html",len(Message),Message)
        except:
            Message = "Internel Error".encode("UTF-8")
            return ("text/html",len(Message),Message)


    def HTTPpipeline(self):
        self.ReciveData()
        Message:tuple[str,int,bytes] = self.HTTPprocessing()#type:ignore
        header = self.formate.format(Message[0],Message[1]).encode("UTF-8")
        final_Message = header+Message[2] #ignore:type
        self.SendData(final_Message,len(final_Message))
        self.sock.close()
        self.alive = False

def makeSocket():
    global sock
    sock = socket.socket()
    sock.bind(("10.12.131.251",8080))
    sock.listen(90)
def connection()->tuple[socket.socket,socket._Address]:
    return sock.accept()
def client(sock:socket.socket,id:int,msg:str):
    HTTPSocket(sock,id,msg)
try :
    makeSocket()

    while(True):
        connections = connection()
        threading.Thread(target=client,args=[connections[0],2,msg]).start()
except :
    sock.close()
    # c1[0].close()
    exit()