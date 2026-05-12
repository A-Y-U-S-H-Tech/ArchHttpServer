"""Copyright (C) 2026  Ayush Mishra"""
"""To Create Coustom HTTP 1v Message for the HTTP server"""
from datetime import datetime

class ResponseHeader():
    def __init__(self) -> None:
        self.header:str = ""
    def SetBaseHeader(self,Header:str): 
        #ADD a header as a base on which further header will be build
        self.header = Header
    def add_Inital(self,Version:str,Satus:str,StatusCode:str):
        #Addition of HTTP version used status and status code
        self.header += "{} {} {}\n".format(Version,StatusCode,Satus)
    def add_Date(self):
        Date = datetime.now().strftime("Date: %a, %d %m %Y %H:%M:%S IST\n")
        self.header += Date

    def Server_Name(self,Name:str):
        #To add the name of server to be shown in the header
        self.header += "Server: {}\n".format(Name)
    
    def Set_ContentType(self,ContentType:str):
        #Add the content type which is being sent
        self.header += "Content-Type: {}\n".format(ContentType)
    
    def Set_ContentLength(self,ContentLength:str):
        #Add the length of the content type which is being send
        self.header += "Content-Length: {}\n".format(ContentLength)
    
    def Set_ConnectionStatus(self,ConectionStatus:str):
        #The Connection Status After Respondse Sending
        self.header += "Connection: {}\r\n\r\n".format(ConectionStatus)

    def ADD_externalHeader(self,header:str):

        self.header += header

    def HeaderPipeline(self):
        pass
        # raise RuntimeError("The Pipeline function has not been implemented")