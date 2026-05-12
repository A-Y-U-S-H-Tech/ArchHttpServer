"""Copyright (C) 2026  Ayush Mishra"""
"""This Module provides varies Base Structure for the Request Handlers"""
from collections.abc import Callable
from HTTPmessageConst import ResponseHeader
import json
from urllib.parse import parse_qs

def GET(func:Callable):
    def Wrapper(Header:str,Message:str)->tuple[str,bytes]:
        return func(Header,Message)
    return Wrapper

def POST(func:Callable):
    def Wrapper(Header:str,Message:str)->tuple[str,bytes]:
        return func(Header,Message)
    return Wrapper


"""####Basic Content Serving Handlers#####"""

@GET
def HTML_Parser(header:str,Message:str)->tuple[str,bytes]:
    resource = header[0:header.index("\r\n",0)].split(" ")[1]
    try :
        html = ''
        _header =ResponseHeader()
        with open("HTML{}".format(resource),"r") as file:
            html = file.read()
        html = html.encode("UTF-8")

        _header.add_Inital("HTTP/1.1","ok","200")
        _header.Set_ContentLength(str(len(html)))
        _header.Set_ContentType("text/html ; charset=UTF-8")

        return (_header.header,html)
    except:
        # self.add_Inital("HTTP/1.1","Unauthorized","401")
        # self.header += "WWW-Authenticate: Basic realm=real"
        _header =ResponseHeader()
        _header.add_Inital("HTTP/1.1","File Not Found","404")
        _Message = "404 File Not Found".encode("UTF-8")
        return (_header.header,_Message)

@GET
def ImageSending(Header:str,Message:str)->tuple[str,bytes]:
    try :
        img = ''
        j = Header.index("\r\n",0)
        resource = Header[0:j].split(" ")[1].split(".")[1]
        _file = Header[0:j].split(" ")[1]
        _header = ResponseHeader()
        with open("IMG{}".format(_file),"br") as file:
            img = file.read()

        _header.add_Inital("HTTP/1.1","OK","200")
        _header.Set_ContentType("image/{}".format(resource))
        _header.Set_ContentLength(str(len(img)))
        return (_header.header,img)
    except:
        _header = ResponseHeader()
        _header.add_Inital("HTTP/1.1","File Not Found","404")
        return (_header.header,b"\0")

@GET
def CSS_Parser(header:str,Message:str)->tuple[str,bytes]:
    resource = header[0:header.index("\r\n",0)].split(" ")[1]
    try :
        css = ''
        _header =ResponseHeader()
        with open("CSS{}".format(resource),"r") as file:
            css= file.read()
        css = css.encode("UTF-8")

        _header.add_Inital("HTTP/1.1","ok","200")
        _header.Set_ContentLength(str(len(css)))
        _header.Set_ContentType("text/css ; charset=UTF-8")

        return (_header.header,css)
    except:
        # self.add_Inital("HTTP/1.1","Unauthorized","401")
        # self.header += "WWW-Authenticate: Basic realm=real"
        _header =ResponseHeader()
        _header.add_Inital("HTTP/1.1","File Not Found","404")
        _Message = "404 File Not Found".encode("UTF-8")
        return (_header.header,_Message)


@POST
def POST_Handler(Header:str,Message:str)->tuple[str,bytes]:
    try:
        _header =ResponseHeader()
        i = Header.index("Content-Type:")
        j = Header.index("\r\n",i)
        post_type = Header[i:j].split(" ")[1]
        with open("test.txt","+a") as file:
            if post_type == "application/x-www-form-urlencoded":
                data = json.dumps(parse_qs(Message),indent=4)
                file.write(data)
                file.close()
                _header.add_Inital("HTTP/1.1","OK","200")
                return (_header.header,b"Message")
            _header.add_Inital("HTTP/1.1","Message Not Supported","405")
            return (_header.header,b"Message")
    except:
        _header =ResponseHeader()
        _header.add_Inital("HTTP/1.1","Internal Server Error","401")
        return (_header.header,b"Message")