from pathlib import Path
import papermill as pm
import yaml


def consultant_names():
    f_consultants = 'data/consultants.yaml'
    with open(f_consultants, 'r') as f:
        consultant_file = yaml.safe_load(f)

    return [k for k, v in consultant_file.items() if v['download']]


def task_init():
    """Initial yaml file generation"""
    return {
        'actions': ['pm.execute_notebook("Consultants.ipynb", "papermill_reports/consultants/Consultants.ipynb")']
    }

    
def task_download():
    """Downloading consulting reports"""     

    consultant_names = consultant_names()

    for consultant_name in consultant_names:
        yield {
            'name': f'{consultant_name}_download',
            'actions': [f'papermill -p consultant_name {consultant_name} "Download.ipynb" "papermill_reports/download/{consultant_name}.ipynb"'],
        }

def task_extract():
    """Extracting entries"""
    for consultant_name in consultant_names:
        yield {
            'name': f'{consultant_name}_extract',
            'actions': [f'papermill -p consultant_name {consultant_name} "Extract.ipynb" "papermill_reports/extract/{consultant_name}.ipynb"'],
            'task_dep': [f'{consultant_name}_download']
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
                'task_dep': [f'{consultant_name}_extract']
            }