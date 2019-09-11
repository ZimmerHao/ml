from libs.utils import generate_hash_by_username_creation_epoch
from datetime import datetime

def test_generate_hash_by_username_creation_epoch():
    exp = "JQnGmmX"
    act = generate_hash_by_username_creation_epoch("wangxisea", datetime(2019,8,22))
    assert exp == act
