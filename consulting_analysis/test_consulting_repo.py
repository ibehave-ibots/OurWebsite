import os
from .consulting_repo import ConsultingResultRepo
import pytest

os.environ['DB_WRITEMODE'] = '1'

@pytest.fixture()
def results(tmp_path):
    results = ConsultingResultRepo.connect(path=tmp_path)
    results.put(short_name='a_b', name='A B', value=2, units='Hertz', display_units='Hz')
    results.put(short_name='c_d', name='C D', value=20, units='Second', display_units='s')
    results.put(short_name='e_f', name='E F', value=-0.5, units='Parts Per Million', display_units='ppm')
    results.save()
    return results


def test_list_method(results):
    results_reports = results.list()
    assert len(results.list()) == 3
    assert results_reports[0].short_name == 'a_b'
    assert results_reports[0].name == 'A B'
    assert results_reports[0].value == 2
    assert results_reports[0].units == 'Hertz'
    assert results_reports[0].display_units == 'Hz'


def test_get_method(results):
    assert results.get('a_b')
    assert not results.get('a_z')
    assert results.get('a_b').name == 'A B'