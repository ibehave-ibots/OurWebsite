
def count_types_of_sessions(consolidated_report, type='short'):
    return consolidated_report.lower().count(f'type: {type}')
 