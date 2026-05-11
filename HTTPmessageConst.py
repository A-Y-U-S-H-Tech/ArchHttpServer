"""Copyright (C) 2026  Ayush Mishra"""
"""To Create Coustom HTTP 1v Message for the HTTP server"""

class Message:
    def __init__(self) -> None:
        self.msg:str = ""

class ResponseHeader(Message):
    def __init__(self) -> None:
        self.header:str = ""
    def 