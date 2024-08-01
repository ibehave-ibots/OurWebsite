from pathlib import Path
import os
from utils import get_reports


consultant_names = [Path(r).stem for r in get_reports()]


def task_download():
    """Downloading raw reports (.docx) files"""
    
    data_dir = "data"
    papermill_dir = "papermill_reports/"
    Path('papermill_reports/download').mkdir(parents=True, exist_ok=True)

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

    papermill_dir = "papermill_reports/"
    Path('papermill_reports/extract').mkdir(parents=True, exist_ok=True)

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
    

def task_upload():
    """Uploading to group_data"""

    papermill_dir = "papermill_reports/"
    Path('papermill_reports/upload').mkdir(parents=True, exist_ok=True)

    in_notebook = "Upload.ipynb" 
    for consultant_name in consultant_names:
        Path(f'papermill_reports/upload/{consultant_name}').mkdir(exist_ok=True)
        entry_nums = [file.stem for file in Path(f'data/entries/{consultant_name}/').glob('*.txt')]
        for entry_num in entry_nums:
            out_name = f"{consultant_name}_{str(entry_num).zfill(3)}_upload"
            out_notebook = os.path.join(papermill_dir, "upload", consultant_name, f"{out_name}.ipynb")
            yield {
                'name': out_name,
                'actions': [f'papermill -p consultant_name {consultant_name} -p entry_num {entry_num} {in_notebook} {out_notebook}'],
                'task_dep': ["extract"],
                'file_dep': Path(f'data/entries/{consultant_name}/').glob('*.txt'),
                'clean': True
            }
