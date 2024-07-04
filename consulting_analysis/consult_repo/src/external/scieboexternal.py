from dataclasses import dataclass
import os
from typing import Union
from dotenv import load_dotenv

@dataclass
class Credentials:
    USR: str
    PWD: str

def load_report_credentials() -> Credentials:
    load_dotenv()
    return Credentials(
        USR = os.getenv('REPORT_USR') or '',
        PWD = os.getenv('REPORT_PWD') or ''
    )

def load_result_credentials() -> Credentials:
    load_dotenv()
    return Credentials(
        USR = os.getenv('RESULT_USR') or '',
        PWD = os.getenv('RESULT_PWD') or ''
    )