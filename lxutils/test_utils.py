from lxutils import *
import doctest
import time
import pytest
import os

def test_timer():
    failures, __ = doctest.testmod(name = 'lxutils.log')
    assert failures == 0

def test_log():
    [log('This is a test 1') for i in range(10000)]
    assert os.stat('log.log').st_size < 50100