#!/usr/local/bin/python3

"""
Module doc: should be before 'import' lines, could be below #! line
A module tells how to use and write python doc, comments, dir, help reltead
utility functions
"""

import sys


def square(x):
    '''
    function doc
    first function def
    '''
    return x ** 2


class Employee:
    '''
    class doc
    first class
    '''
    pass

print(__doc__)              # print self's doc
print(square.__doc__)
print(Employee.__doc__)

print(sys.getrefcount.__doc__)

help(square)                # help(_3_pydoc.square)
help(Employee)              # help(_3_pydoc.Employee)

len(dir([])), len([x for x in dir([]) if not x.startswith('__')])

list_funs = [x for x in dir([]) if not x.startswith('__')]
for x in list_funs:
    print('help(...) on function:', x)
#    help('list.'+x)

