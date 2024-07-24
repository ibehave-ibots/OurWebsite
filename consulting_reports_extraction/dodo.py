from pathlib import Path
import os
from utils import get_reports


papermill_dir = "papermill_reports/"
data_dir = "data"
os.makedirs('papermill_reports/', exist_ok=True)
os.makedirs('papermill_reports/download', exist_ok=True)
os.makedirs('papermill_reports/extract', exist_ok=True)
os.makedirs('papermill_reports/upload', exist_ok=True)
consultant_names = [Path(r).stem for r in get_reports()]

def task_download():
    """Downloading raw reports (.docx) files"""

    for consultant_name in consultant_names:
        in_notebook = "Download.ipynb"        
        out_notebook = Path(os.path.join(papermill_dir, "download", f"{consultant_name}_download.ipynb"))
        out_file = Path(os.path.join(data_dir, "raw", f"{consultant_name}.docx"))
        yield {
            'name': f"{consultant_name}_download",
            'actions': [f"papermill -p consultant_name {consultant_name} {in_notebook} {out_notebook}"],
            'targets': [out_file, out_notebook],
            'file_dep': [in_notebook],
            'clean': True
        }

def task_extract():
    """Extracting entries from downloaded reports"""

    for consultant_name in consultant_names:
        in_notebook = "Extract.ipynb"        
        out_notebook = Path(os.path.join(papermill_dir, "extract", f"{consultant_name}_extract.ipynb"))
        out_file_path = f"data/entries/{consultant_name}/"
        yield {
            'name': f"{consultant_name}_extract",
            'actions': [f"papermill -p consultant_name {consultant_name} {in_notebook} {out_notebook}"],
            'targets': [out_notebook] + list(Path(out_file_path).glob('*.txt')),
            'file_dep': [in_notebook],
            'clean': True
        }
    
