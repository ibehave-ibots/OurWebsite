from dataclasses import dataclass
from typing import Any, Dict
from webdav4.fsspec import WebdavFileSystem
import pandas as pd
from results_repo import ConsultingResultRepo
import os
from dotenv import load_dotenv
from pprint import pprint


@dataclass
class ScieboConsultingStat:
    short_name: str
    name: str
    value: str
    unit: str
    display_unit: str


def from_sciebo() -> Dict[Any, Any]:
    load_dotenv()
    USR = os.getenv('USR')
    fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(USR, ""))
    with fs.open('/consulting_stats.xlsx') as f:
        df = pd.read_excel(f)
    consulting_stat_dict = {
        'short_name':df['short_name'].values,
        'name':df['name'].values,
        'value':df['value'].values,
        'units':df['units'].values,
        'display_units':df['display_units'].values
    } 
    return consulting_stat_dict

def sciebo_to_repo() -> ConsultingResultRepo:
    os.environ['DB_WRITEMODE'] = '1'
    consulting_stat_dict = from_sciebo()
    consulting_repo = ConsultingResultRepo.connect('consulting_data')
    consulting_repo.put_all(consulting_stat_dict)
    return consulting_repo

cs = sciebo_to_repo()
pprint(cs.list())