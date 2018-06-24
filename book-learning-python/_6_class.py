#!/usr/local/bin/python3

"""
A module tells how python class works

ListInstance: list instance attributes with __dict__
ListInherited: list inherited attributes with dir
"""

class ListInstance:
    '''
    Mix-in class that provides a formatted print() or str() of instances via
    inheritance of __str__ coded here; displays instance attrs only; self is
    instance of lowest class; __X names avoid clashing with client's attrs
    '''
    def __attrnames(self):
        result = ''
        for attr in sorted(self.__dict__):
            result += '\t%s=%s\n' % (attr, self.__dict__[attr])
        return result

    def __str__(self):
        return '<Instance of %s, address %s:\n%s>' % (
            self.__class__.__name__,    # class name
            id(self),                   # instance address
            self.__attrnames())         # name=value list

class A(ListInstance):
    pass

def tester(listerclass, sept=False):

    class Super:
        def __init__(self):             # superclass __init__
            self.data1 = 'spam'         # create instance attrs
        def ham(self):
            pass

    class Sub(Super, listerclass):
        def __init__(self):
            Super.__init__(self)
            self.data2 = 'eggs'         # more instance attrs
            self.data3 = 42

        def spam(self):                 # defined another method here
            pass

    instance = Sub()                    # return instance with lister's __str__
    print(instance)
    if sept:
        print('-' * 80)

class ListInherited:
    '''
    Use dir() to collect both instance attrs and names inherited from
    its classes; getattr() fetches inherited names not in self.__dict__;
    use __str__, not __repr__, or else this loops when printing bound
    methods!
    '''
    def __attrnames(self):
        result = ''
        for attr in dir(self):                          # instance dir()
            if attr[:2] == '__' and attr[-2:0] == '__': # skip internals
                result += '\t%s\n' % attr
            else:
                result += '\t%s=%s\n' % (attr, getattr(self, attr))
        return result

    def __str__(self):
        return '<Instance of %s, address %s:\n%s>' % (
            self.__class__.__name__,                    # class name
            id(self),                                   # instance address
            self.__attrnames())                         # name=value list

class ListTree:
    '''
    Mix-in that returns an __str__ trace of the entire class tree and all its
    objects' attrs at and above self; run by print(), str() returns constructed
    string; uses __X attr names to avoid impacting clients; recurse to super-
    classes explicitly, uses str.format() for clarity;
    '''
    def __attrnames(self, obj, indent):
        spaces = ' ' * (indent + 1)
        result = ''
        for attr in sorted(obj.__dict__):
            if attr.startswith('__') and attr.endswith('__'):
                result += spaces + '{0}\n'.format(attr)
            else:
                result += spaces + '{0}={1}\n'.format(attr, getattr(obj, attr))
        return result

    def __listclass(self, aClass, indent):
        dots = '.' * indent
        if aClass in self.__visited:
            return '\n{0}<Class {1}:, address {2}: (see above)>\n'.format(
                dots,
                aClass.__name__,
                id(aClass))
        else:
            self.__visited[aClass] = True
            here = self.__attrnames(aClass, indent)
            above = ''
            for super in aClass.__bases__:
                above += self.__listclass(super, indent + 4)
            return '\n{0}<Class {1}, address {2}:\n{3}{4}{5}>\n'.format(
                dots,
                aClass.__name__,
                id(aClass),
                here, above,
                dots)

    def __str__(self):
        self.__visited = {}
        here = self.__attrnames(self, 0)
        above = self.__listclass(self.__class__, 4)
        return '<Instance of {0}, address {1}:\n{2}{3}>'.format(
            self.__class__.__name__,
            id(self),
            here, above)


if __name__ == '__main__':

    ###########################
    inst = ListInstance()
    print(inst)
    print(dir(inst))                # include instance and class attrs
    print(inst.__dict__)            # instance attrs only - empty

    inst_A = A()
    inst_A.a, inst_A.b, inst_A.c = 1, 2, 3
    print(inst_A)

    tester(ListInstance, True)

    ###########################
    inst_inherited = ListInherited()
    print(inst_inherited)
    print(dir(inst_inherited))
    print(inst_inherited.__dict__)

    tester(ListInherited, True)

    ###########################
    tester(ListTree, True)

