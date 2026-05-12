"""Copyright (C) 2026  Ayush Mishra"""
"""A Basic HTTP Request Pipeline"""
from HTTPmessageConst import ResponseHeader
from Route import Router
import socket

class HTTPSocket(ResponseHeader):
    def __init__(self,sock:socket.socket,route :Router,msg_formate:str):
        self.header:str = ''
        self.sock:socket.socket = sock
        self.router = route
        self.alive = True
        self.recive = ''
        self.send = ''
        self.formate = msg_formate
        self.HTTPpipeline()
    def HeaderPipeline(self,ContentLength:str="0",ContentType:str="\0"):
        self.add_Date()
        self.Server_Name("A Coustom HTTP Server")
        self.Set_ConnectionStatus("Closed")
    
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


    def  HTTPprocessing(self)->tuple[str,bytes]:#router
            i = 0
            j = self.recive[0].index("\n",i)
            Request = self.recive[0][i:j].split(" ")#type:ignore
            print(Request)
            Response = self.router.ExecuteRoute(
                Request[0],Request[1],self.recive[0],self.recive[1])#type:ignore 
    
            if Response == "No Mapping":      
                self.add_Inital("HTTP/1.1","Method Not Supported","404")
                message = "Method Not supported".encode("UTF-8")
                return ("",message)
            else:
                return Response


    def HTTPpipeline(self):
        self.ReciveData()
        print(self.recive[0])
        Message:tuple[str,bytes] = self.HTTPprocessing()#type:ignore
        self.ADD_externalHeader(Message[0])
        self.HeaderPipeline()
        print(self.header)
        header = self.header.encode("UTF-8")
        final_Message = header+Message[1] #ignore:type
        self.SendData(final_Message,len(final_Message))
        self.sock.close()
        self.alive = False