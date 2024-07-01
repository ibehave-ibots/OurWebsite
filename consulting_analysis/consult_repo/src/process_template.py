from dataclasses import dataclass
from docx import Document

@dataclass
class ReportData:
    type: str
    scholar: str
    date: str
    topic: str
    content: str

@dataclass
class TemplateDocumentProcessor:
    reports_path: list

    def process(self) -> list[ReportData]:
        consolidated_reports = []
        for report_path in self.reports_path:
            consolidated_reports.append(self._extract_report_data(report_path))
        return consolidated_reports

    def _extract_report_data(self, report_path):
        document = Document(report_path)
        report_data = self._reset_report_data()
        reports = []
        current_section = None

        for para in document.paragraphs:
            text = para.text.strip()
            
            if text.startswith('Type:'):
                if report_data['type']:
                    reports.append(ReportData(**report_data))
                    report_data = self._reset_report_data()
                report_data['type'] = self._clean_text(text, 'Type:')
                current_section = 'content'
            elif text.startswith('Scholar:'):
                report_data['scholar'] = self._clean_text(text, 'Scholar:')
            elif text.startswith('Date:'):
                report_data['date'] = self._clean_text(text, 'Date:')
            elif text.startswith('Topic:'):
                report_data['topic'] = self._clean_text(text, 'Topic:')
            elif text.startswith('Content:'):
                report_data['content'] = self._clean_text(text, 'Content:')
                current_section = 'content'
            elif current_section == 'content':
                report_data['content'] += '\n' + text

        if report_data['type']:
            reports.append(ReportData(**report_data))

        return reports

    def _clean_text(text, prefix):
        return text.replace(prefix, '').strip()

    def _reset_report_data():
        return {'type': '', 'scholar': '', 'date': '', 'topic': '', 'content': ''}
