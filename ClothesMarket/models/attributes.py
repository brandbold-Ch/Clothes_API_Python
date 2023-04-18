from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional
from bson.objectid import ObjectId


# Primary class
class BaseClass(BaseModel):
    ID: str = Field(alias="ID", default_factory=lambda: str(ObjectId()))
    title: str
    count: int
    size: str
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
    t_shirts: Optional[List[T_Shirts]] = None
    shorts: Optional[List[Shorts]] = None
    shirts: Optional[List[Shirts]] = None
    pants: Optional[List[Pants]] = None
    shoes: Optional[List[Shoes]] = None
    dresses: Optional[List[Dresses]] = None
    footwear: Optional[List[Footwear]] = None


class Clothing_Store(BaseModel):
    _id: str
    women: Optional[Articles] = None
    men: Optional[Articles] = None
    boys: Optional[Articles] = None
    girls: Optional[Articles] = None
    guys: Optional[Articles] = None
    girlsteen: Optional[Articles] = None
