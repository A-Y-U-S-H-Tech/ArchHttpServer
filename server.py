import socket
import time
class Socket(socket.socket,time):
    def __init__(self,Rate,para = None,sock=None):
        self.rate = Rate
        self.connections:socket.socket = None
        if(sock ==None):
            self.sock = self.
        else:
            self.sock = sock
        self.listen(5)
    def Send(self,msg):
        bin_msg = msg.encode("UTF-8")
        msglen = len(bin_msg)
        sent =0
        while sent < msglen:
            s = self.connections.send(bin_msg)
            if s == 0:
                raise RuntimeError("connection Lost")
            sent +=s
    def Recive(self,Metadata):
        recive_Rate = self.rate
        msg = None
        MessLength  = int(self.connections.recv(8).decode("UTF-8").rstrip("\x00"))
        if(Metadata):
            recive_Rate= int(self.connections.recv(8).decode("UTF-8").rstrip("\x00"))
        Recived = 0
        while(Recived < MessLength):
            r = self.connections.recv(recive_Rate)
            Recived+= r
        
    def Listen(self):
        self.connections = self.accept()[0]
            
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
S = Socket(1028,None,s)
# while True:
#     connection,address = s.accept()
#     print(connection,"   ",address)
#     RecvSize = int((connection.recv(8)).decode("UTF-8").rstrip('\x00'))
#     msglen =int(connection.recv(8).decode("UTF-8").rstrip('\x00'))
#     break

# msg = ''
# while len(msg) < msglen:
#     msg+=(connection.recv(RecvSize).decode("UTF-8"))
#     print(msg,'\n')
S.Listen()


S.close()