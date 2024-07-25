from dotenv import load_dotenv
import os
from webdav4.fsspec import WebdavFileSystem
from pathlib import Path
import yaml



def get_reports():
    load_dotenv()
    USR = os.getenv('HASH_USR')
    PWD = os.getenv('HASH_PWD')

    fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(USR, PWD))
    reports = fs.glob('*.docx')
    check_change_yaml = fs.glob('check_change.yaml', detail=False)

    if not check_change_yaml:
        check_change = {}
        check_change = {r:fs.ukey(r) for r in reports}
        yaml_string = yaml.dump(check_change)
        fs.write_text('check_change.yaml', yaml_string)
        return reports

    check_change = yaml.safe_load(fs.read_text(check_change_yaml[0]))
    flag = any([fs.ukey(r) != uk for (r, uk) in check_change.items()])
    if flag:
        change = {r:fs.ukey(r) for r in reports}
        yaml_string = yaml.dump(change)
        fs.write_text('check_change.yaml', yaml_string)
        return reports
    return []

