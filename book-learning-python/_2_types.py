#!/usr/local/bin/python3

import math
import random
import re       # string pattern matching

'''
To view attributes of an object:
> dir(S)                # passed in object
> dir(str)              # passed in type
> dir(list)
> dir(dict)

To see details of a method:
> help(S.replace)       # passed in obj.function
> help(str.replace)     # passed in type.function

To get whole info:
> help(S)               # passed in object
> help(str)             # passed in type
'''

# how many digits?
len(str(2 ** 1000000))

math.pi
random.random()
random.choice(list(range(10)))

# generate consecutive numbers
list(range(10))
list(range(-6, 7, 2))   # [-6, -4, -2, 0, 2, 4, 6]
[[x ** 2, x ** 3] for x in range(4)]

S = 'Spam'
print(S[1])        # p
print(S[1:3])      # pa
print(S[-1])       # m
print(S[1:-1])     # pa
print(S[1:])       # pam
print(S[:3])       # Spa
print(S[:])        # Spam

# string is immutable
S = 'z' + S[1:]     # zpam
S = 'Spam'

# list is mutable
L = list(S)         #
L[1] = 'c'          #
''.join(L)          # join with empty delimiter, Scam

B = bytearray(b'spam')  # bytes list
B.extend(b'eggs')
print(B)
S = B.decode()          # translate to normal string
print(B.decode())       # spameggs

S.find('pa')            # 1
S.replace('pa', 'XYZ')  # sXYZm
print(S.upper())
print(S.isalpha())

line = 'aaa,bbb,ccc,dd'
print(line.split(','))

line += '\n\n'
print(line.rstrip())    # remove white space on the right side
print(line.rstrip().split(','))

S1 = '{0}, eggs, and {1}'.format('spam', 'SPAM!')
S2 = '{}, eggs, and {}'.format('spam', 'SPAM!')
print('S1', '=', S1)
print('S2', '=', S2)

S3 = '{:,.2f}'.format(289423.4221)
print('S3', '=', S3)

S = 'A\nB\tC'
print(len(S))           # 5
ord('\n')               # 10, \n is a byte with binary value 10
S = 'A\0B\0C'           # \0, a binary 0 byte, doesn't terminate string
# non-printables are displayed as \xNN hex escapes
print(S)                # 'A\x00B\x00C'

msg = '''
aaaaaa   aa
bbb '' bbbb""b\tbb
    ccccccc\t
'''
print(msg)

# pattern matching
match = re.match('hello[ \t]*(.*)world', 'hello     python world')
print(match.group(1))   # 'python'

match = re.match('[/:](.*)[/:](.*)[/:](.*)', '/usr/home:jack')
print(match.groups())   # ('usr', 'home', 'jack')

match = re.match('[/:]', '/usr/home/jack')
print(match.groups)

C = re.split('[/:]', '/usr/home/jack')
print(C)                # ['', 'usr', 'home', 'jack']

#
# list
#
L = [123, 'spam', 1.23]
L = L + [1, 2]
L.append('NI')
L.pop(2)                # delete an item in the middle, 2 is the index
L[:]
L[:3]
print([1, 2] in L)      # true

L = ['bb', 'cc', 'aa']
L.sort()
L.reverse()

M = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
M[1]                    # [4, 5, 6]
M[1][2]                 # 6
col2 = [row[1] for row in M]
print(col2 == [2, 5, 8])

col2_even = [row[1]*2 for row in M if row[1] % 2 == 0]
print(col2_even == [4, 16])

diag = [M[i][i] for i in [0, 1, 2]]
print(diag == [1, 5, 9])

# create a generator with (): generalized comprehension
gen = (row[1] for row in M)
next(gen)               # 2
next(gen)               # 5
next(gen)               # 8

# map sum over iterms in M
M_sum = list(map(sum, M))   # [6, 15, 24]

#
# dictionary
#
D = {}                                                      # by assignment
D['name'] = 'bob'
D['job'] = 'dev'
D['age'] = 20
D1 = dict(name='bob', job='dev', age=30)                    # by keyword
D2 = dict(zip(['name', 'job', 'age'], ['bob', 'dev', 50]))  # by zipping

rec = {'name': {'first': 'bob', 'last': 'smith'},
       'jobs': ['dev', 'mgr'],
       'age': 40.5}
print(rec)
print(rec['name'])
print(rec['name']['last'])
print(rec['jobs'][-1])

D = {'a': 1, 'b': 2, 'c': 3}
ks = list(D.keys())
ks.sort()
for key in ks:
    print(key, '=>', D[key])

#
# tuple
#
T = (2, 5, 7, 1, 3)
len(T)                  # 5
T + (5, 6)              # tuple is immutable
T = T[:] + (2,)         # (2, 5, 7, 1, 3, 2)
T.count(2)              # 2

#
# set
#
X = set('spam')         # any python version
Y = {'h', 'a', 'm'}     # >= 2.7
X - Y
X & Y
X ^ Y
X | Y
print(X > Y)
print(list(X))          # ['m','p','a','s']

#
# type(), isinstance()
#
print(type(X))
print(type(D))
if isinstance(X, set):
    print("'X' is set")
if isinstance(T, tuple):
    print("'T' is tuple")


