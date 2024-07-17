from __future__ import annotations

from datetime import datetime
from typing import Literal
from pydantic import BaseModel
from yaml_dir_parser import load_dir

class Data(BaseModel):
    consulting_reports: dict[str, ConsultingReport]

class ConsultingReport(BaseModel):
    consultant: str
    content: str
    date: datetime
    scholar: str
    topic: str
    type: Literal['short', 'hands']


data = load_dir('output_yaml')
Data.model_validate(data)