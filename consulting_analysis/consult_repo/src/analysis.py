from __future__ import annotations
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    short_name: str
    name: str
    value: float
    units: str
    display_units: str


def count_types_of_sessions(report: str, type: str = 'short') -> AnalysisResult:
    counts = report.lower().count(f'type: {type}')
    return AnalysisResult(
        short_name=f'n_{type}',
        name=f'Total number of {type} chats',
        value=counts,
        units='Session',
        display_units='Session'
    )

