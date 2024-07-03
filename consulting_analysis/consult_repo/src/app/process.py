from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from docx import Document

@dataclass
class ReportData:
    type: str
    scholar: str
    date: str
    topic: str
    content: str

@dataclass
class Consultant:
    name: str
    reports: list[ReportData]

    @property
    def scholars(self) -> list[str]:
        return {report.scholar for report in self.reports}

    @property
    def num_total_sessions(self) -> int:
        return len(self.reports)

    @property    
    def num_short_sessions(self) -> int:
        return sum(1 for report in self.reports if report.type == 'short')

    @property    
    def num_hands_on_sessions(self) -> int:
        return sum(1 for report in self.reports if report.type == 'hands')
    
    @property
    def num_unique_scholars(self) -> int:
        scholars = {report.scholar for report in self.reports}
        return len(scholars)
    
    @property
    def time_short_hrs(self) -> float:
        return sum(1 for report in self.reports if report.type == 'short')*0.75

    @property
    def time_hands_on_hrs(self) -> float:
        return sum(1 for report in self.reports if report.type == 'hands')*2.5
    
    @property
    def time_all_hrs(self) -> float:
        return self.time_short_hrs + self.time_hands_on_hrs
 
    @property
    def consolidated_content(self) -> str:
        return " ".join(report.content for report in self.reports)
    
    @property
    def consolidated_topic(self) -> str:
        return " ".join(report.topic for report in self.reports)


class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, reports_path: list) -> list[ReportData]:
        ...

@dataclass
class TemplateDocumentProcessor(DocumentProcessor):
    def process(self, reports_path: list) -> list[ReportData]:
        consultants = []
        
        for report_path in reports_path:
            consultants.append(
                Consultant(
                    name = Path(report_path).stem,
                    reports = self._extract_report_data(report_path)
                )                
            )
        return consultants

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

    def _clean_text(self, text, prefix):
        return text.replace(prefix, '').strip()

    def _reset_report_data(self):
        return {'type': '', 'scholar': '', 'date': '', 'topic': '', 'content': ''}