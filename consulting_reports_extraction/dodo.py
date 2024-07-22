from pathlib import Path

consultant_names = ['sangeetha', 'mohammad', 'nick']

def task_download():
    """Downloading consulting reports"""

    for consultant_name in consultant_names:
        download_files = [f'data/raw/{consultant_name}.docx']

        def check_uptodate():
            return all(Path(file).exists for file in download_files)

        yield {
            'name': f'{consultant_name}_download',
            'actions': [f'papermill -p consultant_name {consultant_name} "Download.ipynb" "papermill_reports/download/{consultant_name}.ipynb"'],
            'targets': download_files,
            'uptodate': [check_uptodate]
        }

def task_extract():
    """Extracting entries"""
    for consultant_name in consultant_names:
        extract_files = [file for file in Path('data/entries/{consultant_name}/').glob('*.txt')]

        def check_uptodate():
            return all(Path(file).exists for file in extract_files)

        yield {
            'name': f'{consultant_name}_extract',
            'actions': [f'papermill -p consultant_name {consultant_name} "Extract.ipynb" "papermill_reports/extract/{consultant_name}.ipynb"'],
            'targets': extract_files,
            'uptodate': [check_uptodate]
        }

def task_upload():
    """Upload entries"""
    for consultant_name in consultant_names:
        yield {
            'name': f'{consultant_name}_upload',
            'actions': [f'papermill -p consultant_name {consultant_name} "Upload.ipynb" "papermill_reports/upload/{consultant_name}.ipynb"'],
        }