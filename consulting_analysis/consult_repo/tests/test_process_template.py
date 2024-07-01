import pytest
from pytest import approx
from src import TemplateDocumentProcessor
from fsspec.implementations.local import LocalFileSystem
from pathlib import Path

@pytest.fixture
def template():
    return TemplateDocumentProcessor()
    
@pytest.fixture
def reports(download_raw):
    fs_raw = LocalFileSystem()
    reports = fs_raw.ls(str(download_raw))
    return reports

@pytest.fixture
def sandbox_report(reports):
    for report in reports:
        if Path(report).stem == 'consulting_session_template':
            return report


def test_process_return_template(reports):
    assert any(Path(report).stem == 'consulting_session_template' for report in reports)

def test_process_for_template(template, sandbox_report):
    consultant = template.process([sandbox_report])[0]
    assert consultant.name == 'consulting_session_template'
    assert consultant.num_total_sessions == 16
    assert consultant.num_short_sessions == 11
    assert consultant.num_hands_on_sessions == 5
    assert consultant.num_unique_scholars == 13
    assert consultant.time_short_hrs == approx(8.25)
    assert consultant.time_hands_on_hrs == approx(12.5)
    assert consultant.time_all_hrs == approx(20.75)
    

    