from lxutils import *
import doctest
import time
import pytest

def test_timer():
    failures, __ = doctest.testmod(name = 'lxutils.log')
    assert failures == 0

@pytest.fixture(scope='module')
def get_bitrix():
    return Bitrix("https://ctrlcrm.bitrix24.ru/rest/1/0agnq1xt4xv1cqnc/")


def test_bitrix(get_bitrix):
    b = get_bitrix
    deals = b.get_list('crm.deal.list')
    assert len(deals) > 1000

def test_bitrix_semaphore_start_stop(get_bitrix):
    b = get_bitrix
    t1 = time.monotonic()
    deals1 = b.get_list('crm.deal.list')
    assert b._sw._sem._value < 100
    t2 = time.monotonic()
    deals2 = b.get_list('crm.deal.list')
    t3 = time.monotonic()
    assert t3 - t2 < t2 - t1

def test_bitrix_short_lists(get_bitrix):
    b = get_bitrix
    assert len(b.get_list('crm.dealcategory.stage.list')) <= 50
    assert len(b.get_list('user.get')) <= 50

def test_bitrix_post(get_bitrix):
    b = get_bitrix
    r = b.post_list('crm.contact.add', [{'fields': {
        'NAME': 'Алексей',
        'LAST_NAME': 'Лещенко',
        "PHONE": [{"VALUE": "+79852227949", "VALUE_TYPE": "WORK"}] 	
    }}])
    assert r != None
    r2 = b.post_list('crm.contact.delete', [{'ID': r[0]['result']}])
    assert r2 != None
