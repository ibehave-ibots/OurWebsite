from pathlib import Path
import papermill as pm
import os

papermill_dir = "papermill_reports/"

def task_init():
    """Generating data/consultants.yaml"""
    out_notebook = Path(os.path.join(papermill_dir, "consultants", "Consultants.ipynb"))    
    out_file = Path('data/consultants.yaml')
    def run_papermill():
        pm.execute_notebook('Consultants.ipynb', out_notebook)

    return {
        'actions': [run_papermill],
        'targets': [out_notebook, out_file],
        'file_dep': ["Consultants.ipynb"],
        'clean': True
    }