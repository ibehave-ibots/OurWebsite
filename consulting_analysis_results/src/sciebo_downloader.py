from dataclasses import dataclass
from typing import Any, Dict
from webdav4.fsspec import WebdavFileSystem
import pandas as pd
from results_repo import ConsultingResultRepo
import os
from dotenv import load_dotenv


@dataclass
class ScieboConsultingStat:
    short_name: str
    name: str
    value: str
    unit: str
    display_unit: str


def get_from_sciebo() -> None:
    load_dotenv()
    USR = os.getenv('USR')
    fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(USR, ""))
    fs.download("/", "consulting_data", recursive=True)    

def from_xlsx(path: str = 'consulting_data/consulting_stats.xlsx') -> Dict[Any, Any]:
    df = pd.read_excel(path)
    consulting_stat_dict = {
        'short_name':df['short_name'].values,
        'name':df['name'].values,
        'value':df['value'].values,
        'units':df['units'].values,
        'display_units':df['display_units'].values
    }
    
    return consulting_stat_dict

def sciebo_to_repo():
    os.environ['DB_WRITEMODE'] = '1'
    get_from_sciebo()
    consulting_stat = from_xlsx()
    consulting_repo = ConsultingResultRepo.connect('consulting_data')
    consulting_repo.from_dict(consulting_stat)
    return consulting_repo.list()

print(sciebo_to_repo())