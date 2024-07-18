from __future__ import annotations
from datetime import datetime

from pydantic import BaseModel, EmailStr, HttpUrl, FilePath
from typing import Optional, Literal


class Data(BaseModel):
    consulting_reports: Optional[dict[str, ConsultingReport]] = None
    images: dict[str, FilePath]
    orgs: Orgs
    people: dict[str, Person]
    group: GroupInfo
    skills: dict[str, Skill]
    technologies: dict[str, Technology]


class GroupInfo(BaseModel):
    short_description: str
    address: str
    email: EmailStr
    mailing_list_subscribe_url: HttpUrl
    history: list[MilestoneEvent]


class MilestoneEvent(BaseModel):
    date: datetime
    name: str
    short_description: str


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

class ConsultingReport(BaseModel):
    consultant: str
    content: str
    date: datetime
    scholar: str
    topic: str
    type: str #Literal['short', 'hands']