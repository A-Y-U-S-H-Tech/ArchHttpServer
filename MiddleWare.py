"""Copyright (C) 2026  Ayush Mishra"""
"""A Basic MiddleWare Framework for ArchHTTP Server"""
from collections.abc import Callable
def MiddleWare(function:Callable): 
    def Wrapper(Header:str,Message:str)->tuple[bool,str,bytes|str]:
        return function(Header,Message)
    return Wrapper


class Middleware():
    def __init__(self) -> None:
        self.MiddleWare:list = []
    def add_MiddleWare(self,MiddleWare:Callable):
        self.MiddleWare.append(MiddleWare)
    def Excetute_MiddleWare(self,Header:str,Message:bytes|str)->tuple[bool,str,bytes|str]:
        _Header = Header
        _Message= Message
        for MiddleWare in self.MiddleWare:
            response = MiddleWare(_Header,_Message)
            _Header = response[1]
            _Message = response[2]
            if response[0]:
                return (True,_Header,_Message)
        return (False,_Header,_Message)