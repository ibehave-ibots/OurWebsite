import yaml
from dotenv import load_dotenv
import os
from webdav4.fsspec import WebdavFileSystem

load_dotenv()

SANGEE_REPORT_USR = os.getenv('SANGEE_REPORT_USR')
SANGEE_REPORT_PWD = os.getenv('SANGEE_REPORT_PWD')

with open('data/group.yaml') as group_f:
    group = yaml.safe_load(group_f)

fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_REPORT_USR, SANGEE_REPORT_PWD))
reports = fs.ls("/", detail=False)
fs.download("/", ".", recursive=True)

# with open('sangee_report.txt', 'r') as report:
#     content = report.read()

# num_short_chat = content.lower().count('type: short chat')
# num_hands_on = content.lower().count('type: hands-on')
# num_consulting_sessions = num_short_chat + num_hands_on
# total_hours_consulting = round(num_short_chat*0.75 + num_hands_on*2.5)

# group["consulting_stats"]["num_consulting_sessions"] = num_consulting_sessions
# group["consulting_stats"]["total_hours_consulting"] = total_hours_consulting

# with open('data/group.yaml', 'w') as update_group_f:
#     yaml.safe_dump(group, update_group_f, default_flow_style=False)

