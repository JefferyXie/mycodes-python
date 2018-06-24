#!/usr/local/bin/python3

"""
A module tells how python function works, including function's arguments
"""

import os
import sys
import math

def fun_min(*args):
    ''' Find the min value '''
    # not necessary, let python raise exception if no args
    if not args:
        return None
    res = args[0]
    for arg in args[1:]:
        if arg < res:
            res = arg
    return res

print(fun_min(3, 4, 1, 2))
print(fun_min('bb', "aa"))
print(fun_min([2, 2], [1, 1], [4, 4]))
print(fun_min())

def fun_minmax(comparator, *args):
    '''
    Find min or max value in terms of comparator
    '''
    res = args[0]
    for arg in args[1:]:
        if comparator(arg, res):
            res = arg
    return res

def comparator_lessthan(x, y): return x < y
def comparator_grtrthan(x, y): return x > y

print(fun_minmax(comparator_lessthan, 4, 2, 1, 5, 6, 3))
print(fun_minmax(comparator_grtrthan, 4, 2, 1, 5, 6, 3))

def fun_print1(*args, **kargs):
    '''
    Print by using keyword argument matching
    fun_print(*args, sep=' ', end='\n', file=sys.stdout)
    '''
    sep = kargs.get('sep', ' ')
    end = kargs.get('end', '\n')
    file = kargs.get('file', sys.stdout)
    output = ''
    first = True
    for arg in args:
        output += ('' if first else sep) + str(arg)
        first = False
    file.write(output + end)

fun_print1(1, 2, 3)
fun_print1(1, 2, 3, sep='')
fun_print1(1, [2], (3,), sep='..')
fun_print1()


def fun_print2(*args, sep=' ', end='\n', file=sys.stdout):
    '''
    Print by using keyword-only arguments in Python3
    '''
    output = ''
    first = True
    for arg in args:
        output += ('' if first else sep) + str(arg)
        first = False
    file.write(output + end)

fun_print2(1, 2, 3, 4, 5)
try:
    fun_print2(99, name='bob')
except Exception as ex:
    print(str(ex))

def fun_print3(*args, **kargs):
    '''
    Print by using keyword args deletion with defaults
    '''
    sep = kargs.pop('sep', ' ')
    end = kargs.pop('end', '\n')
    file = kargs.pop('file', sys.stdout)
    if kargs:
        raise TypeError('extra keywords: %s' % kargs)
    output = ''
    first = True
    for arg in args:
        output += ('' if first else sep) + str(arg)
        first = False
    file.write(output + end)

try:
    fun_print3(99, name='bob')
except Exception as ex:
    print(ex)

################################################################################
#
#               map, filter, reduce
#
################################################################################
counters = range(1, 5)
def inc(x): return x + 10

# map results in iterable obj
print(list(map(inc, counters)))

print(list(map(lambda x: x + 5, counters)))
print(list(map(lambda x: x + 5, [1, 2, 3, 4])))

# 1**2, 2**3, 3**4
print(list(map(pow, [1, 2, 3], [2, 3, 4])))

# filter results in iterable obj
print(list(filter(lambda x: x > 0, range(-5, 5))))
print([x for x in range(-5, 5) if x > 0])

import functools, operator
# reduce returns a single result
print(functools.reduce(lambda x, y: x + y, [1, 2, 3, 4])) # 1+2+3+4
print(functools.reduce(lambda x, y: x * y, [1, 2, 3, 4])) # 1*2*3*4

# utilize built-in operators
print(functools.reduce(operator.add, [2, 4, 6]))
print(functools.reduce(operator.mul, [2, 4, 6]))

################################################################################
#
#               generator
#
################################################################################
def gensquares(N):
    for i in range(N):
        yield i ** 2

gen_x = gensquares(4)
print(gen_x)
print(next(gen_x))
print(next(gen_x))
print(next(gen_x))
print(next(gen_x))

def ups(line):
    for sub in line.split(','):
        yield sub.strip().upper()

# tuple takes all elements of generator
print(tuple(ups(' aa, bb ,  cc c  cc ')))
# generator works for enumerate
print({i:s for (i, s) in enumerate(ups('a aa , bb, cc c'))})

# showcase how generator.send() works
# send() method does two things:
# 1) advance to next item;
# 2) caller pass some value to generator - yield expression
def gen():
    for i in range(5):
        x = yield i
        print('from gen():', 'x=',  x, 'i=', i)

G = gen()
print(next(G))      # call next() to start generator
print(next(G))      # advanced, but caller doesn't send value to yield expression
print(next(G))      # x=None
print(next(G))      # x=None

G = gen()
print(next(G))
print(G.send(77))   # advanced, and send 77 to yield expression, x=77
print(G.send(88))   # advanced, and send 88 to yield expression, x=88
print(next(G))      # advanced, but no value sent, x= None

'''
generator expression vs. list comprehension

generator expression is just like normal list comprehension, it supports all the
syntax but it is enclosed in parentheses instead of square brackets
'''
# list comprehension: build a list
list_comp = [x ** 2 for x in range(4)]
print(list_comp)
# generator expression: make an iterable
gen_comp = (x ** 2 for x in range(4))
print(gen_comp)

# wrap a generator expression in a list built-in call to force it to produce all
# its result in a list at a once
print(list(x ** 2 for x in range(4)))
print(list(gen_comp))


def fun_dir_walk(dir = '.'):
    '''
    At each level of a tree, yields a tuple of current directory, subdir and files
    '''
    print('Walk directory:', dir)
    for (root, subs, files) in os.walk(dir):
        print('root=%s, subs=%s, files=%s' % (root, subs, files))
        for name in files:
            if name.startswith('call'):
                print(root, name)

fun_dir_walk()
fun_dir_walk('../../mycodes-python')

def fun_permute1(seq):
    '''
    List permutation, return all items after the call
    '''
    if not seq:
        return [seq]
    else:
        res = []
        for i in range(len(seq)):
            rest = seq[:i] + seq[i+1:]
            for x in fun_permute1(rest):
                res.append(seq[i:i+1] + x)
        return res

def fun_permute2(seq):
    '''
    List permutation, return generator which works better for large permutation
    '''
    if not seq:
        yield seq
    else:
        for i in range(len(seq)):
            rest = seq[:i] + seq[i+1:]
            for x in fun_permute2(rest):
                yield seq[i:i+1] + x

list_perm = 'abcd'
print(fun_permute1(list_perm))
print(list(fun_permute2(list_perm)))
print([x for x in fun_permute2(list_perm)])

print('math.factorial(10):', math.factorial(10))    # 10*9*8*.....*1
perm_10_1 = fun_permute1(list(range(10)))   # take long time
print(len(perm_10_1))                       # should equal to math.factorial(10)

perm_10_2 = fun_permute2(list(range(10)))   # return immediately
perm_10_2 = list(perm_10_2)
print(perm_10_1 == perm_10_2)               # TRUE

################################################################################
#
#               coding your own map, zip
#
################################################################################

def fun_mymap1(func, *seqs):
    '''
    My own map with classic coding pattern
    '''
    res = []
    for args in zip(*seqs):
        res.append(func(*args))
    return res

def fun_mymap2(func, *seqs):
    '''
    My own map with list comprehension
    '''
    return [func(*args) for args in zip(*seqs)]

def fun_mymap3(func, *seqs):
    '''
    My own map returns generator
    '''
    for args in zip(*seqs):
        yield func(*args)

def fun_mymap4(func, *seqs):
    '''
    My own map returns generator - one line code
    '''
    return (func(*args) for args in zip(*seqs)) # parenthesis gives generator

S1, S2, S3 = list(range(-2, 3)), [1, 2, 3], [2, 3, 4, 5]
print(list(fun_mymap1(abs, S1)))
print(list(fun_mymap1(pow, S2, S3)))
print(list(fun_mymap2(abs, S1)))
print(list(fun_mymap2(pow, S2, S3)))
print(list(fun_mymap3(abs, S1)))
print(list(fun_mymap3(pow, S2, S3)))
print(list(fun_mymap4(abs, S1)))
print(list(fun_mymap4(pow, S2, S3)))

def fun_myzip1(*seqs):
    '''
    My own zip returns generator
    '''
    seqs = [list(S) for S in seqs]
    while all(seqs):
        yield tuple(S.pop(0) for S in seqs)

def fun_myzip2(*seqs):
    '''
    My own zip returns list
    '''
    minlen = min(len(S) for S in seqs)
    return [tuple(S[i] for S in seqs) for i in range(minlen)]

S1, S2 = 'abc', 'xyz123'
print(list(fun_myzip1(S1, S2)))
print(fun_myzip2(S1, S2))

