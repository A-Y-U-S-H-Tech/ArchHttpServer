"""Copyright (C) 2026  Ayush Mishra"""
"""A Basic MiddleWare Framework for ArchHTTP Server"""
from collections.abc import Callable
def MiddleWare(function:Callable): 
    def Wrapper(Header:str,Message:str)->tuple[bool,str,bytes]:
        return function(Header,Message)
    return Wrapper