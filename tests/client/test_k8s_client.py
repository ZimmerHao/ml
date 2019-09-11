import pytest
from libs.kubernetes.client import generate_hash_by_username

def test_generate_hash_by_username():
    username = 'tony@dp.com'
    timestamp = 1559053316
    exp_hash = '45OWXzY'
    assert generate_hash_by_username(username, timestamp) == exp_hash