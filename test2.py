class a:
    def __init__(self) -> None:
        self.route =[]
    def add_route(self,naem):
        self.route.append(naem)

class b:
    def __init__(self,a) -> None:
        self.a:a = a #type:ignore
    def kkk(self):
        self.a.add_route(naem=self.kkk)

A = a()
B = b(A)
B.kkk()
A.add_route("Meow")
A.add_route("rat")
C = b(A)
print(list(route for route in C.a.route))
print(list(route for route in B.a.route))