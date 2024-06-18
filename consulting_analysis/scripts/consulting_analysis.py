from results_repo import ConsultingResultRepo
from fsspec.implementations.local import LocalFileSystem
from utils.consulting_utils import count_types_of_sessions, count_num_unique_scholars, count_num_consultants, count_num_occurrances_of_word
import os
import sys
from pathlib import Path


def process_consolidated_report(consolidated_report):
    n_consultants = count_num_consultants()

    n_short = count_types_of_sessions(consolidated_report, type='short')
    num_short_per_consultant = n_short / n_consultants
    short_hrs = n_short * 0.45
    hrs_short_per_consultant = short_hrs / n_consultants
    
    n_hands_on = count_types_of_sessions(consolidated_report, type='hands')
    num_hands_per_consultant = n_hands_on / n_consultants
    hands_on_hrs = n_hands_on * 2.5
    hrs_hands_per_consultant = hands_on_hrs / n_consultants
    
    n_sess = n_short + n_hands_on
    tot_hrs = short_hrs + hands_on_hrs
    n_unique_scholars = count_num_unique_scholars(consolidated_report)

    n_python = count_num_occurrances_of_word(consolidated_report, word='python')
    n_matlab = count_num_occurrances_of_word(consolidated_report, word='matlab')
    
    return {
        'n_sess': ('Total number of sessions', n_sess, 'Session', 'Session'),
        'tot_hrs': ('Total hours of sessions', tot_hrs, 'Hour', 'Hrs'),
        'n_short': ('Total number of short chats', n_short, 'Session', 'Session'),
        'short_hrs': ('Total time of short chats', short_hrs, 'Hour', 'Hrs'),
        'hands_on_hrs': ('Total time of hands-on sessions', hands_on_hrs, 'Hour', 'Hrs'),
        'n_hands': ('Total number of hands-on sessions', n_hands_on, 'Session', 'Session'),
        'n_unique_scholars': ('Number of different scholars', n_unique_scholars, 'Researcher', 'Session'),
        'n_consultants': ('Number of consultants', n_consultants, 'Consultant', 'Consultant'),
        'num_short_per_consultant': ('Average short chats per consultant', num_short_per_consultant, 'Session', 'Session'),
        'hrs_short_per_consultant': ('Average time in short chats per consultant', hrs_short_per_consultant, 'Hour', 'Hrs'),
        'num_hands_per_consultant': ('Average hands-on per consultant', num_hands_per_consultant, 'Session', 'Session'),
        'hrs_hands_per_consultant': ('Average time in hands-on per consultant', hrs_hands_per_consultant, 'Hour', 'Hrs'),
        'n_python': ('Number of Python mentions', n_python, 'Occurance', 'Occurance'),
        'n_matlab': ('Number of Matlab mentions', n_matlab, 'Occurance', 'Occurance'),
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
