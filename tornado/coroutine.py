#!/usr/bin/env python

#
# https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-dokk
# https://stackoverflow.com/questions/27043076/tornado-coroutine
#

import os,sys,time,threading
import functools
from tornado import gen
from tornado.ioloop import IOLoop

print('python version=' + sys.version)

def print_thread_id():
    print('### {0}'.format(threading.get_ident()))


###############################################################################
#
###############################################################################
@gen.coroutine
def func():
    print('[{0}] {1} starts...'.format(threading.get_ident(), func.__name__))
    # 0) foo() will be executed when encounting below yield
    # 1) if replacing with 'time.sleep(6)', it'll block main thread so foo()
    # won't be triggered unless func() is done
    # 2) if don't have keyword 'yield', 'gen.sleep(6)' won't cause any sleep
    yield gen.sleep(6.0)
    print('[{0}] {1} ends, {2}'.format(threading.get_ident(), func.__name__, 6))


@gen.coroutine
def foo():
    print('[{0}] {1} starts...'.format(threading.get_ident(), foo.__name__))
    yield gen.sleep(2)
    print('[{0}] {1} ends, {2}'.format(threading.get_ident(), foo.__name__, 2))


@gen.coroutine
def call():
    print('[{0}] {1} starts...'.format(threading.get_ident(), call.__name__))
    yield gen.sleep(0)
    print('[{0}] {1} ends, {2}'.format(threading.get_ident(), call.__name__, 0))


@gen.coroutine
def main1(ioloop):
    ioloop.call_later(5, call)
    yield [func(), foo()]
    print('[{0}] main1 done.'.format(threading.get_ident()))
    #print('%(name)s done.'%{'name': main.__name__})


###############################################################################
#
###############################################################################
class HelloHandler():
    @gen.coroutine
    def run(self):
        print('[{0}] {1}: before yield'.format(
            threading.get_ident(), self.run.__name__))
        x = yield self.do_test()
        # below part won't be executed unless 'do_test()' finishes, this case
        # is different from above case 'yield [func(), foo()]'
        print('[{0}] {1}: after yield, ret={2}'.format(
            threading.get_ident(), self.run.__name__, x))

    @gen.coroutine
    def do_test(self):
        print('[{0}] {1}: entered...'.format(
            threading.get_ident(), self.do_test.__name__))
        yield time.sleep(3)
        print('[{0}] {1}: done...'.format(
            threading.get_ident(), self.do_test.__name__))
        return 'do_test'

    @gen.coroutine
    def run_forever(self):
        count = 1
        while True:
            print('[{0}] {1}: before yield {2}'.format(
                threading.get_ident(), self.run_forever.__name__, count))
            x = yield self.do_test()
            print('[{0}] {1}: after yield {2}'.format(
                threading.get_ident(), self.run_forever.__name__, count))
            count += 1
            time.sleep(2)


def main2():
    handler = HelloHandler()

    # start event loop, execute, and stop loop
    IOLoop.current().run_sync(handler.run)

    # handle 'run_forever' in separate route (not necessary different thread)
    IOLoop.current().spawn_callback(handler.run_forever)
    print('[{0}] main2(): after spawn_callback...'.format(
        threading.get_ident()))
    IOLoop.current().start()

    print('[{0}] main2(): done.'.format(threading.get_ident()))


###############################################################################
#
###############################################################################
if __name__ == '__main__':
    print_thread_id()

    ioloop = IOLoop.current()
    main_f = functools.partial(main1, ioloop=ioloop)
    #ioloop.run_sync(main_f)

    main2()

    print('all done.')

