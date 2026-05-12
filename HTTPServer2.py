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
global image_formate_supported
image_formate_supported = ("jpg","png") #read only writing forbidden 
msg = """HTTP/1.1 200 OK\nDate: Tue, 05 May 2026 12:00:00 GMT\nServer: custom HTTP Server\nContent-Type: {}; charset=UTF-8\nContent-Length: {}\nConnection: close\r\n\r\n"""




def makeSocket():
    global sock
    sock = socket.socket()
    sock.bind(("10.12.131.251",8081))
    sock.listen(90)
def connection()->tuple[socket.socket,socket._Address]:
    return sock.accept()
def client(sock:socket.socket,route:Router,msg:str):
    HTTPSocket(sock,route,msg)
r1 = Router()
r1.add_Route("GET","/home.html",HTML_Parser)
r1.add_Route("GET","/form.html",HTML_Parser)
r1.add_Route("GET","/test.html",HTML_Parser)
r1.add_Route("GET","/style.css",CSS_Parser)
r1.add_Route("POST","/submit-form",POST_Handler)
r1.add_Route("GET","/test.jpg",ImageSending)
r1.add_Route("GET","/test.png",ImageSending)
try :
    makeSocket()

    while(True):
        connections = connection()
        threading.Thread(target=client,args=[connections[0],r1,msg]).start()
except :
    sock.close()
    # c1[0].close()
    exit()