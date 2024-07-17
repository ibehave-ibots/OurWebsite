import shutil
import os
from pathlib import Path

ip_dir = 'output_yaml/consulting_reports'
op_dir = 'group_data_test/consult_reports'

ip_dir_path = Path(ip_dir)
op_dir_path = Path(op_dir)

if not ip_dir_path.exists():
    raise FileNotFoundError(f"{ip_dir_path} not found")

if not op_dir_path.exists():
    op_dir_path.mkdir(parents=True)

for file in ip_dir_path.glob(pattern='*.yaml'):
    shutil.copy(file, op_dir_path)
