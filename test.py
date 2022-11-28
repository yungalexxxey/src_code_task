import pytest
import requests


def test_request_with_no_response():
    assert requests.get('http://0.0.0.0:1337/?request=такого_нет_совсем').json() == {}


def test_request_with_one_index_returned():
    assert len(requests.get('http://0.0.0.0:1337/?request=шины').json().keys()) == 1


def test_request_with_two_index_returned():
    assert len(requests.get('http://0.0.0.0:1337/?request=кухня').json().keys()) == 2

pytest.fail('')