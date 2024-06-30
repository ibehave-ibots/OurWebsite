from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

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

def count_num_unique_scholars(report: str) -> AnalysisResult:
    consolidated_list = report.split('\n')
    consolidated_list_empty_string_remove = list(filter(None, consolidated_list))
    scholar_names = []
    for i in range(len(consolidated_list_empty_string_remove) - 1):  
        if "Scholar(s):" in consolidated_list_empty_string_remove[i]:
            next_element = consolidated_list_empty_string_remove[i + 1]
            if not (next_element.startswith("Meeting topic") or next_element.startswith("\t")):
                scholar_names.append(next_element)
    df = pd.DataFrame({'scholars': scholar_names})
    return AnalysisResult(
        short_name='n_unique_scholars',
        name='Number of different scholars',
        value=len(df),
        units='Researcher',
        display_units='Researcher'
    )


def count_num_occurrances_of_word(report, word='python') -> AnalysisResult:
    return AnalysisResult(
        short_name=f"n_{word}",
        name=f"Number of {word} mentions",
        value=report.lower().count(word),
        units='Occurrance',
        display_units='Occurrance'
    )