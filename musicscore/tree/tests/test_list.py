class A(object):
    """"""
    a = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.b = []


class B(A):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class C(A):
    """"""
    a = ['a', 'b']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# a = A()
#
# b = B()
# b.a.append(1)
#
# bb = B()
# bb.a.append(2)
#
# c = C()
# print(a.a)
# print(b.a)
# print(bb.a)
# print(c.a)
# c.a.append('c')
# print(a.a)
# print(b.a)
# print(bb.a)
# print(c.a)
