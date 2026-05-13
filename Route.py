"""Copyright (C) 2026  Ayush Mishra """
"""A HTTP Route Mapper and helper for my HTTP Web Server"""
from collections.abc import Callable

class Router:
    def __init__(self) -> None:
        self.route:dict[tuple[str,str],tuple[Callable,bool]] = {}
        self.MiddleWareRoute:dict[tuple[str,str],list[Callable]]={}
    def add_Route(self,Method:"str",url:str,MEthodFunc:Callable,MiddleWareHint=False):
        self.route[(Method,url)] = (MEthodFunc,MiddleWareHint)
    def ExecuteRoute(self,Method:str,url:str,Header:str,Message:str):
        try:
            route = self.route[((Method,url))]
            if route[1]:
                return route[0](Method,url,Header,Message)
            else:  
                return route[0](Header,Message)   
        except:
            return "No Mapping"
    def addMiddleWare(self,Method:str,url:str,MiddleWare:list[Callable],Handler:Callable,MiddleWareHint=False):
        MiddleWare.append(Handler)
        self.MiddleWareRoute[(Method,url)] = MiddleWare
    def ExecuteMiddleWare(self,Method:str,url:str,Header:str,Message:str):
        try:
            MiddleWare = self.MiddleWareRoute[(Method,url)]
            for i in range(len(MiddleWare)-1):
                response = MiddleWare[i](Header,Message)
                if(not response[0]):
                    return (response[1],response[2])
            return MiddleWare[len(MiddleWare)-1](Header,Message)
        except:
            return "No Mapping"