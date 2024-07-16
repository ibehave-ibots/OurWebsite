import papermill as pm
import shutil

params = {
    'raw_dir': 'raw',
    'output_dir': 'output_yaml'
}


in_notebook = 'reports_to_yaml.ipynb'
out_notebook = 'reports_papermill/output.ipynb'

pm.execute_notebook(
    in_notebook,
    out_notebook,
    params
)

