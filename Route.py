"""Copyright (C) 2026  Ayush Mishra """
"""A HTTP Route Mapper and helper for my HTTP Web Server"""
from collections.abc import Callable


class Router:
    def __init__(self) -> None:
        self.route:dict[tuple[str,str],Callable] = {}
    def add_Route(self,Method:"str",url:str,MEthodFunc:Callable):
        self.route[(Method,url)] = MEthodFunc
    def ExecuteRoute(self,Method:str,url:str,Header:str,Message:str):
        try:
            return self.route[((Method,url))](Header,Message)   
        except:
            return "No Mapping"