"""
>>> import time
>>> log()
Traceback (most recent call last):
...
TypeError: log() missing 1 required positional argument: 'msg'

>>> log('a')
202...: a

>>> log('b') # повторный вызов показывает время, прошедшее с прошлого вызова
202...: b, +0:00:...s

>>> with timer('c'):
...     time.sleep(1)
202...: c: starting, +0:00:...s
202...: c: finished in 0:00:01...s

>>> with timer('1'):
...     with timer('2'):
...         log('3')
...         time.sleep(1)
...     log('4')
...     time.sleep(2)
202...: 1: starting, +0:00:...s
202...: 2: starting, +0:00:00s
202...: 3, +0:00:00s
202...: 2: finished in 0:00:01...s
202...: 4, +0:00:00s
202...: 1: finished in 0:00:03...s
"""

from datetime import datetime as dt

lastlog = 0

def log(msg):
    global lastlog
    now = dt.now()
    if lastlog == 0:
        print (f'{now.strftime("%Y-%m-%d %H:%M:%S")}: {msg}')
    else:
        print ('{}: {}, +{}s'.format(
            now.strftime("%Y-%m-%d %H:%M:%S"),
            msg,
            str(now - lastlog)
        ))
    lastlog = now
    return None

class timer:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        global lastlog
        now = dt.now()
        self.start = now
        if lastlog == 0:
            print (f'{now.strftime("%Y-%m-%d %H:%M:%S")}: {self.msg}: starting')
        else:
            print ('{}: {}: starting, +{}s'.format(
                now.strftime("%Y-%m-%d %H:%M:%S"),
                self.msg,
                str(now - lastlog)
            ))
        lastlog = now

    def __exit__(self, a1, a2, a3):
        global lastlog
        now = dt.now()
        print('{}: {}: finished in {}s'.format(
            now.strftime("%Y-%m-%d %H:%M:%S"),
            self.msg,
            str(now - self.start)))
        lastlog = now

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
