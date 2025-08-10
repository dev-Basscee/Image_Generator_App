import os
from fastapi import Header, HTTPException

class User:
    def __init__(self, id: str):
        self.id = id

def require_api_key(x_api_key: str = Header(None)):
    key = os.getenv("API_KEY")
    if not x_api_key or x_api_key != key:
        raise HTTPException(401, "Unauthorized")
    return User(id="default-user")