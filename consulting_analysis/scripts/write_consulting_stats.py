from results_repo import ConsultingResultRepo
from fsspec.implementations.local import LocalFileSystem
from utils.consulting_utils import count_types_of_sessions, count_num_unique_scholars
import os
import sys
from pathlib import Path

def process_consolidated_report(consolidated_report):
    n_short = count_types_of_sessions(consolidated_report, type='short')
    short_hrs = n_short * 0.45
    n_hands_on = count_types_of_sessions(consolidated_report, type='hands')
    hands_on_hrs = n_hands_on * 2.5
    n_sess = n_short + n_hands_on
    tot_hrs = short_hrs + hands_on_hrs
    n_unique_scholars = count_num_unique_scholars(consolidated_report)
    
    return {
        'n_sess': ('Total number of sessions', n_sess, 'Session', 'Session'),
        'tot_hrs': ('Total hours of sessions', tot_hrs, 'Hour', 'Hrs'),
        'n_hands': ('Total number of hands-on sessions', n_hands_on, 'Session', 'Session'),
        'n_unique_scholars': ('Number of different scholars', n_unique_scholars, 'Researcher', 'Session')
    }

def main(consolidated_report_path):
    os.environ['DB_WRITEMODE'] = '1'

    with open(consolidated_report_path, 'r', encoding='utf-8') as f:
        consolidated_report = f.read()

    fs_local = LocalFileSystem()
    repo_local = ConsultingResultRepo.connect(fs_local)

    results = process_consolidated_report(consolidated_report)

    for short_name, (name, value, units, display_units) in results.items():
        repo_local.put(
            short_name=short_name,
            name=name,
            value=value,
            units=units,
            display_units=display_units
        )    

    repo_local.push()
   

if __name__ == "__main__":
    input_path = sys.argv[1]
    main(input_path)
