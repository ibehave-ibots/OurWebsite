from datetime import datetime
from typing import Literal
from pydantic import BaseModel
import yaml
from fsspec.implementations.local import LocalFileSystem


class Reports(BaseModel):
    consultant: str
    content: str
    date: datetime
    scholar: str
    topic: str
    type: Literal['short', 'hands']

fs = LocalFileSystem()
reports = fs.ls('output_yaml', detail=False)


for report in reports:
    with open(report) as f:
        report_dict = yaml.safe_load(f)
        Reports(**report_dict)

