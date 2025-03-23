from pydantic import BaseModel
from typing import List,Optional

# Base schema for Blog
class Blog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True  # Enable ORM compatibility for SQLAlchemy models

# Base schema for User creation
class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True  # Enable ORM compatibility

# Schema to show User details with their blogs
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]  # Reference the Blog schema here

    class Config:
        orm_mode = True  # Enable ORM compatibility

# Schema to show Blog details with its creator
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser  # Reference the ShowUser schema here

    class Config:
        orm_mode = True  # Enable ORM compatibility

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
