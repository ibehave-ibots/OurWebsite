from . consulting_repo import ConsultingResult, ConsultingResultRepo
import pytest

a = ConsultingResult(
    short_name='n_sess',
    name='Number of Sessions',
    value=100,
    units='Sessions',
    display_units='Sess'
)

b = ConsultingResult(
    short_name='tot_hours',
    name='Total Number of Hours',
    value=10.5,
    units='Hour',
    display_units='Hrs'
)

c = ConsultingResult(
    short_name='n_sc',
    name='Number of Short Chats',
    value=50,
    units='Session',
    display_units='Sess'
)

@pytest.fixture
def results():
    results = ConsultingResultRepo(
        consulting_results=(a, b)
    )
    return results


def test_repo_has_two_results(results):
    assert len(results.consulting_results) == 2

def test_put_method_adds_result(results):
    results.put(c)
    assert len(results.consulting_results) == 3

def test_get_method_returns_n_sess_when_called(results):
    n_sess = results.get('n_sess')
    assert n_sess.short_name == 'n_sess'
    assert n_sess.name == 'Number of Sessions'
    assert n_sess.value == 100.0

def test_len_clear_all_deletes_all_values_in_list(results):
    assert len(results.consulting_results) == 2
    results.clear_all()
    assert len(results.consulting_results) == 0

