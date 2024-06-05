import yaml
from dotenv import load_dotenv
import os
from webdav4.fsspec import WebdavFileSystem
from docx import Document
from docx.oxml.ns import qn

load_dotenv()
SANGEE_REPORT_USR = os.getenv('SANGEE_REPORT_USR')
SANGEE_REPORT_PWD = os.getenv('SANGEE_REPORT_PWD')

def count_page_breaks(doc, pattern='___'):
    page_break_count = 0
    pages = []
    current_text = ""

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run._r.xpath('.//w:br[@w:type="page"]'):
                page_break_count += 1
                if pattern in current_text:
                    pages.append(current_text.split(pattern)[0].strip())
                else:
                    pages.append(current_text.strip())
                current_text = ""
            else:
                current_text += run.text + '\n'
    
    if current_text.strip():
        if pattern in current_text:
            pages.append(current_text.split(pattern)[0].strip())
        else:
            pages.append(current_text.strip())

    return page_break_count, pages


with open('data/group.yaml') as group_f:
    group = yaml.safe_load(group_f)

fs = WebdavFileSystem("https://uni-bonn.sciebo.de/public.php/webdav", auth=(SANGEE_REPORT_USR, SANGEE_REPORT_PWD))
reports = fs.ls("/", detail=False)
fs.download("/", ".", recursive=True)

num_consulting_sessions = 0
session_reports = []
for report in reports:
    doc = Document(report)
    num_session, session_report = count_page_breaks(doc)
    num_consulting_sessions += num_session
    session_reports.extend(session_report)

num_short_chat = 0
num_hands_on = 0


for session_report in session_reports:
    num_short_chat += session_report.lower().count('type: short')
    num_hands_on += session_report.lower().count('type: hands')

total_hours_consulting = round(num_short_chat*0.75 + num_hands_on*2.5)
group["consulting_stats"]["num_consulting_sessions"] = num_consulting_sessions
group["consulting_stats"]["total_hours_consulting"] = total_hours_consulting

with open('data/group.yaml', 'w') as update_group_f:
    yaml.safe_dump(group, update_group_f, default_flow_style=False)

