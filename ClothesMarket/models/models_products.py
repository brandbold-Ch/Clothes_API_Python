from pydantic import BaseModel, Field
from typing import List, Optional
from bson.objectid import ObjectId


# Primary class
class BaseClass(BaseModel):
    _id: str = lambda: str(ObjectId())
    title: str
    count: int
    size: str
    price: int
    colors: List[str]
    image: str
    gender: str
    age_range: int


# Sons
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
    t_shirts: List[dict]
    shorts: List[dict]
    shirts: List[dict]
    pants: List[dict]
    shoes: List[dict]
    dresses: List[dict]
    footwear: List[dict]


class Clothing_Store(BaseModel):
    _id: str
    women: Optional[Articles] = None
    men: Optional[Articles] = None
    boys: Optional[Articles] = None
    girls: Optional[Articles] = None
    guys: Optional[Articles] = None
    girlsteen: Optional[Articles] = None
