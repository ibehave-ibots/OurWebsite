consultant_names = ['sangeetha', 'mohammad', 'nick']

def task_download():
    """Downloading consulting reports"""
    for consultant_name in consultant_names:
        yield {
            'name': f'{consultant_name}_download',
            'actions': [f'papermill -p consultant_name {consultant_name} "Download.ipynb" "papermill_reports/download/{consultant_name}.ipynb"']
        }

def task_extract():
    """Extracting entries"""
    for consultant_name in consultant_names:
        yield {
            'name': f'{consultant_name}_extract',
            'actions': [f'papermill -p consultant_name {consultant_name} "Extract.ipynb" "papermill_reports/extract/{consultant_name}.ipynb"'],
            'task_dep': ['download']
        }
