class a:
    def __init__(self) -> None:
        self.route =[]
    def add_route(self,naem):
        self.route.append(naem)

class b:
    def __init__(self,a) -> None:
        self.a:list = a #type:ignore
    def kkk(self,b):
        self.a.append(b)

A = []
B = b(A)
B.kkk(1)
A.append("Meow")
A.append("rat")
C = b(A)
print(list(route for route in C.a))
print(list(route for route in B.a))