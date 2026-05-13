"""Copyright (C) 2026  Ayush Mishra"""


import socket 
import os
import threading 
from urllib.parse import parse_qs
import json
from HTTPmessageConst import ResponseHeader
from Route import Router
from Handler import GET,POST,HTML_Parser,CSS_Parser,ImageSending,POST_Handler
from HTTPSocket import HTTPSocket
from MiddleWare import MiddleWare,Middleware
import base64
global image_formate_supported
image_formate_supported = ("jpg","png") #read only writing forbidden 
msg = """HTTP/1.1 200 OK\nDate: Tue, 05 May 2026 12:00:00 GMT\nServer: custom HTTP Server\nContent-Type: {}; charset=UTF-8\nContent-Length: {}\nConnection: close\r\n\r\n"""

@MiddleWare
def Auth(Header:str,Message:str)->tuple[bool,str,bytes]:
    if "Authorization" in Header:
        i = Header.index("Authorization:")
        j = Header.index("\n",i)
        Credential = base64.b64decode(Header[i:j].split(" ")[2]).decode("UTF-8").split(":")
        if(Credential[0] == "ayush" and Credential[1] == "123456789"):
            return (True,"",b"")
    _header = ResponseHeader()
    _header.add_Inital("HTTP/1.1","Forbiden","401")
    _header.ADD_Basic_Auth("Protected Content")
    return (False,_header.header,b"")

@MiddleWare
def logging(Header:str,Message:str)->tuple[bool,str,bytes]:
    with open("log.txt","+a")as file:
        file.write("Header:-\n")
        file.write(Header)
        file.write("\n")
        file.write("Message:\n")
        if(Message != None):
            if(type(Message) == bytes):
                file.write("Message in bytes:\n")
                with open("log.txt","+ab")as file2:
                    file2.write(Message)
            else:
                file.write(Message)
        else:
            file.write("NONE\n")
    return (True,"",b"")

@MiddleWare
def PHPRC_Loger(Header:str,Message:str)->tuple[bool,str,bytes|str]:
    with open("log.txt","+a")as file:
        file.write("Header:-\n")
        file.write(Header)
        file.write("\n")
        file.write("Message:\n")
        if(Message != None):
            if(type(Message) == bytes):
                file.write("Message in bytes:\n")
                file.close()
                with open("log.txt","+ab")as file2:
                    file2.write(Message)
            else:
                file.write(Message)
        else:
            file.write("NONE\n")
    return (False,Header,Message)
@MiddleWare
def Protected(Header:str,Message:str)->tuple[bool,str,str|bytes]:
    j = Header.index("\r\n",0)
    url = Header[0:j].split(" ")
    _header = ResponseHeader()
    if(url[1] != "/EP.html"):
        _header.add_Inital("HTTP/1.1","The file is protected","401")
        return (True,_header.header,b"")
    return (False,Header,Message)

def makeSocket():
    global sock
    sock = socket.socket()
    sock.bind(("10.12.131.251",8080))
    sock.listen(90)
def connection()->tuple[socket.socket,socket._Address]:
    return sock.accept()
def client(sock:socket.socket,route:Router,PRMW,PHMW):
    HTTPSocket(sock,route,PRMW,PHMW)
r1 = Router()
r1.add_Route("GET","/home.html",HTML_Parser)
r1.add_Route("GET","/form.html",HTML_Parser)
r1.add_Route("GET","/test.html",HTML_Parser)
r1.add_Route("GET","/style.css",CSS_Parser)
r1.add_Route("POST","/submit-form",POST_Handler)
r1.add_Route("GET","/test.jpg",ImageSending)
r1.add_Route("GET","/test.png",ImageSending)
r1.addMiddleWare("GET","/EP.html",[logging,Auth],HTML_Parser)
r1.add_Route("GET","/EP.html",r1.ExecuteMiddleWare,True)
PRMW = Middleware()
PHMW = Middleware()
PRMW.add_MiddleWare(Protected)
PRMW.add_MiddleWare(PHPRC_Loger)
PHMW.add_MiddleWare(PHPRC_Loger)
# PHMW.add_MiddleWare(Protected)
try :
    makeSocket()

    while(True):
        connections = connection()
        threading.Thread(target=client,args=[connections[0],r1,PRMW,PHMW]).start()
except :
    sock.close()
    # c1[0].close()
    exit()