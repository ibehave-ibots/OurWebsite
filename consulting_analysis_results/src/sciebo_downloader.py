from dataclasses import dataclass
from typing import Any, Dict
from webdav4.fsspec import WebdavFileSystem
import pandas as pd


@dataclass
class ScieboConsultingStat:
    short_name: str
    name: str
    value: str
    unit: str
    display_unit: str


def get_from_sciebo(usr: str = "fZKODDtYVAnP0pk") -> None:
    fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(usr, ""))
    fs.download("/", "consulting_data", recursive=True)    

def from_xlsx(path: str = 'consulting_data/consulting_stats.xlsx') -> ScieboConsultingStat:
    df = pd.read_excel(path)
    consulting_stat = ScieboConsultingStat(
        short_name=df['short_name'].values,
        name=df['name'].values,
        value=df['value'].values,
        unit=df['unit'].values,
        display_unit=df['display_unit'].values
    )
    return consulting_stat

print(from_xlsx())