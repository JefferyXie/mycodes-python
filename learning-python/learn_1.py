#!/usr/local/bin/python3
import sys
import os

version = sys.version_info.major
print("Running python version:", version)

print(sys.platform)
print(os.getcwd())
print(2 ** 100)

# input() in version 2 is same as eval(input()) in version 3
if version >= 3:
    input()                             # wait for any input
else:
    raw_input()

x = 'Spam!'
print(x * 5)

for c in x:
    print(c)

print('Run', 'away!', '...')            # 3.x function
# print 'Run', 'away more!', '...'      # 2.x statement

'''
# multiple ways to run this script
import learn_1                          # will run the script once

from imp import import reload
reload(learn_1)                         # newly reload script and run once

exec(open('learn_1.py').read())         # newly open the script file and run once
'''
