from results_repo import ConsultingResultRepo
from fsspec.implementations.local import LocalFileSystem
from utils.consulting_utils import count_types_of_sessions
import os
import sys
from pathlib import Path

def main(consolidated_report_path):
    os.environ['DB_WRITEMODE'] = '1'

    with open(consolidated_report_path, 'r', encoding='utf-8') as f:
        consolidated_report = f.read().replace('\n', '')

    fs_local = LocalFileSystem()
    repo_local = ConsultingResultRepo.connect(fs_local)

    n_short = count_types_of_sessions(consolidated_report, type='short')
    short_hrs = n_short * 0.45
    n_hands_on = count_types_of_sessions(consolidated_report, type='hands')
    hands_on_hrs = n_hands_on * 2.5
    n_sess = n_short + n_hands_on
    tot_hrs = short_hrs + hands_on_hrs

    repo_local.put(
        short_name='n_sess',
        name='Total number of sessions',
        value=n_sess,
        units='Session',
        display_units='Session'
    )

    repo_local.put(
        short_name='tot_hrs',
        name='Total hours of sessions',
        value=tot_hrs,
        units='Hour',
        display_units='Hrs'
    )

    repo_local.put(
        short_name='n_hands',
        name='Total number of hands-on sesions',
        value=n_hands_on,
        units='Session',
        display_units='Session'
    )
    repo_local.push()
   

if __name__ == "__main__":
    input_path = sys.argv[1]
    main(input_path)
