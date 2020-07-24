from lxutils import *
import doctest

def test_timer():
    failures, __ = doctest.testmod(name = 'lxutils.log')
    assert failures == 0