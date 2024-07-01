from dataclasses import dataclass
from docx import Document

@dataclass
class ReportData:
    type: str
    scholar: str
    date: str
    topic: str
    content: str

def clean_text(text, prefix):
    return text.replace(prefix, '').strip()

def reset_report_data():
    return {'type': '', 'scholar': '', 'date': '', 'topic': '', 'content': ''}

def extract_report_data(file_path):
    document = Document(file_path)
    report_data = reset_report_data()
    reports = []
    current_section = None

    for para in document.paragraphs:
        text = para.text.strip()
        
        if text.startswith('Type:'):
            if report_data['type']:
                reports.append(ReportData(**report_data))
                report_data = reset_report_data()
            report_data['type'] = clean_text(text, 'Type:')
            current_section = 'content'
        elif text.startswith('Scholar:'):
            report_data['scholar'] = clean_text(text, 'Scholar:')
        elif text.startswith('Date:'):
            report_data['date'] = clean_text(text, 'Date:')
        elif text.startswith('Topic:'):
            report_data['topic'] = clean_text(text, 'Topic:')
        elif text.startswith('Content:'):
            report_data['content'] = clean_text(text, 'Content:')
            current_section = 'content'
        elif current_section == 'content':
            report_data['content'] += '\n' + text

    if report_data['type']:
        reports.append(ReportData(**report_data))

    return reports

file_path = 'Sangee_template.docx'
reports = extract_report_data(file_path)
print(reports[1].content)
