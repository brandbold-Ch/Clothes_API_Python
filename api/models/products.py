from pydantic import BaseModel
from typing import Optional
from bson.objectid import ObjectId


# Primary class
class BaseClass(BaseModel):
    _ID: str
    title: str
    count: int
    size: list[str]
    price: int
    colors: list[str]
    image: str
    gender: str
    age_range: list[int]


# Son's
class T_Shirts(BaseClass):
    pass


class Shorts(BaseClass):
    pass


class Shirts(BaseClass):
    pass


class Pants(BaseClass):
    pass


class Shoes(BaseClass):
    pass


class Dresses(BaseClass):
    pass


class Footwear(BaseClass):
    pass


# Secondary class or class market
class Articles(BaseModel):
    t_shirts: list[dict]
    shorts: list[dict]
    shirts: list[dict]
    pants: list[dict]
    shoes: list[dict]
    dresses: list[dict]
    footwear: list[dict]


class Clothing_Store(BaseModel):
    _id: str
    name_branch: str
    women: Optional[Articles] = None
    men: Optional[Articles] = None
    boys: Optional[Articles] = None
    girls: Optional[Articles] = None
    guys: Optional[Articles] = None
    girls_teen: Optional[Articles] = None
