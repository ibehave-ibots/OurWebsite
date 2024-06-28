from dataclasses import dataclass
from docx import Document

@dataclass
class ReportData:
    type: str
    scholar: str
    date: str
    topic: str
    content: str

def extract_report_data(file_path):
    document = Document(file_path)
    report_data = {
        'type': '',
        'scholar': '',
        'date': '',
        'topic': '',
        'content': ''
    }

    current_section = None
    reports = []

    for para in document.paragraphs:
        text = para.text.strip()
        
        if text.startswith('Type:'):
            if current_section == 'content':  
                reports.append(
                    ReportData(
                        type=report_data['type'],
                        scholar=report_data['scholar'],
                        date=report_data['date'],
                        topic=report_data['topic'],
                        content=report_data['content']
                    )
                )

                report_data = {
                    'type': '',
                    'scholar': '',
                    'date': '',
                    'topic': '',
                    'content': ''
                }
            report_data['type'] = text.replace('Type:', '').strip()
            current_section = 'type'
        elif text.startswith('Scholar:'):
            report_data['scholar'] = text.replace('Scholar:', '').strip()
            current_section = 'scholar'
        elif text.startswith('Date:'):
            report_data['date'] = text.replace('Date:', '').strip()
            current_section = 'date'
        elif text.startswith('Topic:'):
            report_data['topic'] = text.replace('Topic:', '').strip()
            current_section = 'topic'
        elif text.startswith('Content:'):
            report_data['content'] = text.replace('Content:', '').strip()
            current_section = 'content'
        elif current_section == 'content':
            report_data['content'] += '\n' + text

    if report_data['type']:
        reports.append(
            ReportData(
                type=report_data['type'],
                scholar=report_data['scholar'],
                date=report_data['date'],
                topic=report_data['topic'],
                content=report_data['content']
            )
        )

    return reports

file_path = 'consulting_session_template.docx'
reports = extract_report_data(file_path)
