import pytest
from read_write_interface import ConsultingSession, ConsultingSessionList


john = ConsultingSession(
    date="2024-01-01",
    name="John Smith",
    type='Short Chat',
    consultant='Mike',
    duration_mins=250
)

jane = ConsultingSession(
    date="2024-01-01",
    name="Jane Smith",
    type='Hands-on',
    consultant='Mock',
    duration_mins=250
)

def test_correct_names_in_sessions():
    consulting_sessions = ConsultingSessionList(
        sessions = [john, jane]
    )

    assert consulting_sessions.sessions[0].name == 'John Smith'
    assert consulting_sessions.sessions[1].name == 'Jane Smith'

def test_file_names_are_correct(tmp_path):
    consulting_sessions = ConsultingSessionList(
        sessions = (john, jane)
    )

    consulting_sessions.write_to_directory(tmp_path)
    written_file_paths = list(tmp_path.iterdir())
    written_file_names = [file.name for file in written_file_paths]

    assert len(written_file_paths) == 2
    assert 'JohMik2024-01-01.json' in written_file_names
    assert 'JanMoc2024-01-01.json' in written_file_names