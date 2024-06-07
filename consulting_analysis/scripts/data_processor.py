from docx import Document


def count_page_breaks(doc, pattern='___'):
    pages = []
    current_text = ""

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run._r.xpath('.//w:br[@w:type="page"]'):
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

    return pages

def create_consolidated_report(reports):
    session_reports = []
    for report in reports:
        doc = Document(report)
        session_report = count_page_breaks(doc)
        session_reports.extend(session_report)

    consolidated_report = ' '.join(session_reports)
    return consolidated_report