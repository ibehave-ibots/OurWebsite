from docx import Document

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

    for para in document.paragraphs:
        text = para.text.strip()
        
        if text.startswith('Type:'):
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

    return report_data

file_path = 'consulting_session_template.docx'
report_data = extract_report_data(file_path)
print(report_data['content'])
