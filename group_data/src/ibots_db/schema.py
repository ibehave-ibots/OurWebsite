from __future__ import annotations

from pydantic import BaseModel, EmailStr, HttpUrl, FilePath
from typing import Optional, Literal


class Data(BaseModel):
    people: dict[str, Person]
    orgs: Orgs
    skills: dict[str, Skill]
    technologies: dict[str, Technology]
    images: dict[str, FilePath]


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


class Orgs(BaseModel):
    partners: list[Partner]


class Partner(BaseModel):
    name: str
    url: HttpUrl
    email: EmailStr
    description: str
    institute: Institute


class Institute(BaseModel):
    name: str
    url: HttpUrl


class Skill(BaseModel):
    name: str
    icon: str
    short_description: str


class Technology(BaseModel):
    name: str
    icon: str
    homepage: HttpUrl

