from __future__ import annotations

from pydantic import BaseModel, EmailStr, HttpUrl, FilePath
from typing import Optional, Literal
from yaml_dir_parser import load_dir

class Data(BaseModel):
    people: dict[str, Person]

class Person(BaseModel):
    name: str
    nickname: str
    role: Literal['current', 'past', 'other']
    photo: HttpUrl | FilePath
    email: Optional[EmailStr] = None
    booking_url: Optional[HttpUrl] = None
    field_of_study: Optional[str] = None
    github_username: Optional[str] = None
    image: Optional[HttpUrl | FilePath] = None

    



data = load_dir('data')
dd = {}
dd['people'] = data['people']
Data.model_validate(dd)
# UserModel.model_validate(data)