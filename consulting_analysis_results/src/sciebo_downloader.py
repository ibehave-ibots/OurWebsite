from typing import Any, Dict
from webdav4.fsspec import WebdavFileSystem
import pandas as pd

def get_from_sciebo(usr: str = "fZKODDtYVAnP0pk") -> None:
    fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(usr, ""))
    fs.download("/", "consulting_data", recursive=True)    

def from_xlsx(path: str = 'consulting_data/consulting_stats.xlsx') -> Dict[str, Dict[Any, Any]]:
    df = pd.read_excel(path)
    return df.to_dict()

from_xlsx()