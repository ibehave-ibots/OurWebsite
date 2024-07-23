from pathlib import Path
import papermill as pm

pm.execute_notebook('Consultants.ipynb', 'papermill_reports/consultants/Consultants.ipynb')
with open('data/consultants.txt', 'r') as f:
    names = f.readlines()
consultant_names = [name.strip() for name in names]
    
def task_download():
    """Downloading consulting reports"""       
    for consultant_name in consultant_names:
        yield {
            'name': f'{consultant_name}_download',
            'actions': [f'papermill -p consultant_name {consultant_name} "Download.ipynb" "papermill_reports/download/{consultant_name}.ipynb"'],
            'targets': [f"papermill_reports/download/{consultant_name}.ipynb", f"data/raw/{consultant_name}.docx"],
            'file_dep': ['data/consultants.txt']
        }

def task_extract():
    """Extracting entries"""
    for consultant_name in consultant_names:
        yield {
            'name': f'{consultant_name}_extract',
            'actions': [f'papermill -p consultant_name {consultant_name} "Extract.ipynb" "papermill_reports/extract/{consultant_name}.ipynb"'],
            'task_dep': ['download']
        }

def task_upload():
    """Upload entries"""

    for consultant_name in consultant_names:
        Path(f'papermill_reports/upload/{consultant_name}').mkdir(exist_ok=True)
        extract_files = [file for file in Path(f'data/entries/{consultant_name}/').glob('*.txt')]
        for file in extract_files:
            yield {
                'name': f'{consultant_name}_{file.stem}_upload',
                'actions': [f'papermill -p consultant_name {consultant_name} -p entry_num {file.stem} "Upload.ipynb" "papermill_reports/upload/{consultant_name}/{file.stem}.ipynb"'],
                'task_dep': ['extract']
            }