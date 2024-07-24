from pathlib import Path
import papermill as pm
import os

import yaml

papermill_dir = "papermill_reports/"
data_dir = "data"
os.makedirs('papermill_reports/', exist_ok=True)
os.makedirs('papermill_reports/download', exist_ok=True)
os.makedirs('papermill_reports/extract', exist_ok=True)
os.makedirs('papermill_reports/upload', exist_ok=True)



def task_download():
    """Downloading raw reports (.docx) files"""

    consultants_info = get_consultants()
    consultant_names = list(consultants_info.keys())

    for consultant_name in consultant_names:        
        out_notebook = Path(os.path.join(papermill_dir, "download", f"{consultant_name}_download.ipynb"))
        out_file = Path(os.path.join(data_dir, "raw", f"{consultant_name}.docx"))
        if consultants_info[consultant_name]['is_changed']:
            yield {
                'name': f"{consultant_name}_download",
                'actions': [f"papermill -p"],
                'targets': [],
                'file_dep': [consultants_file,],
                'task_dep': ['init'],
                'clean': True,
                'uptodate': [False]
            }