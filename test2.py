def Get(a):
    def wrapper():
        print("before function\n")
        a()
        print("after function\n")
    return wrapper

@Get
def hello():
    print("hello world")
@Get
def meow():
    print("MEOW")
meow()