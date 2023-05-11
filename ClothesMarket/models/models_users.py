from pydantic import BaseModel


class Users(BaseModel):
    _id: str
    username: str
    password: str
