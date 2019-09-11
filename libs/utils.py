from hashids import Hashids
from datetime import datetime

def generate_hash_by_username_creation_epoch(user_account: str, created_at: datetime = datetime(2019,8,22)) -> str:
    hashed_username = Hashids(salt=user_account).encode(int(created_at.timestamp()))
    return hashed_username