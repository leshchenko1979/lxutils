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
import logging, logging.handlers
import os, sys

handler = logging.handlers.RotatingFileHandler("log.log", maxBytes=10000, backupCount=0, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel("INFO")
root.addHandler(handler)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
root.addHandler(handler)

log = root.info
exception = root.exception

class timer:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        now = dt.now()
        self.start = now
        log (f'{self.msg}: starting')

    def __exit__(self, a1, a2, a3):
        now = dt.now()
        log('{}: finished in {}s'.format(
            self.msg,
            str(now - self.start)))

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
