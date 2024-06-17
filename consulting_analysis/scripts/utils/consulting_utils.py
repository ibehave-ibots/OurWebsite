
import pandas as pd


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