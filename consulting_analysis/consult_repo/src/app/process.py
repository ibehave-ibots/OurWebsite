from abc import ABC, abstractmethod
from dataclasses import dataclass


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
