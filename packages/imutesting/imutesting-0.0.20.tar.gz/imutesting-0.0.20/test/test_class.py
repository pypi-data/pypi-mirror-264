class MyClass:
    def __init__(self, a, b, **kwargs):
        print('1')
        print(a)
        print('2')
        c = kwargs.get("param3")
        print('3')
        print(c)
        print('4')
        d = Class(b,**kwargs)
        print('5')
        print(kwargs)


class Class:
    def __init__(self, b, **kwargs):
        # kwargs是一个字典，包含了所有传递给构造函数的关键字参数
        print('6')
        print(b)
        print('7')
        a=kwargs.get("param2")
        print('8')
        print(a)
        print('9')
        print(kwargs)


if __name__ == "__main__":
    obj = MyClass(13,18,param1=10, param2='hello', param3=[1, 2, 3])
