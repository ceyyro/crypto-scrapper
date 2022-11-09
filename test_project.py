import pytest
from project import *

# Need to first use this function in order to get the API values which functions below use
scrape()


def test_i():
    assert get_i('BTC') == 0
    assert get_i('BNB') == 3
    with pytest.raises(IndexError) as whatever:
        get_i('huj')
    assert whatever.type == IndexError

def test_name():
    assert get_name(0) == 'bitcoin'
    assert get_name(3) == 'bnb'
    with pytest.raises(IndexError) as whatever:
        get_name(13)
    assert whatever.type == IndexError

def test_scrape():
    assert scrape() == 0
