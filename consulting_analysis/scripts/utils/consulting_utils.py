
import pandas as pd

from data_downloader import connect_to_sciebo

def count_num_consultants():
    fs = connect_to_sciebo()
    return len(fs.ls('/'))

def count_types_of_sessions(consolidated_report, type='short'):
    return consolidated_report.lower().count(f'type: {type}')
 
def count_num_unique_scholars(consolidated_report):
    consolidated_list = consolidated_report.split('\n')
    consolidated_list_empty_string_remove = list(filter(None, consolidated_list))
    scholar_names = []
    for i in range(len(consolidated_list_empty_string_remove) - 1):  
        if "Scholar(s):" in consolidated_list_empty_string_remove[i]:
            next_element = consolidated_list_empty_string_remove[i + 1]
            if not (next_element.startswith("Meeting topic") or next_element.startswith("\t")):
                scholar_names.append(next_element)
    df = pd.DataFrame({'scholars': scholar_names})
    return len(df.scholars.unique())

def count_num_occurrances_of_word(consolidated_report, word='python'):
    return consolidated_report.lower().count(word)