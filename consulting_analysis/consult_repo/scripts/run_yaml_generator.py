import papermill as pm

params = {
    'raw_dir': 'raw',
    'output_dir': 'output_yaml'
}


in_notebook = 'reports_to_yaml.ipynb'
out_notebook = 'output.ipynb'

pm.execute_notebook(
    in_notebook,
    out_notebook,
    params
)