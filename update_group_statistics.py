import yaml
from pprint import pprint

with open('data/group.yaml') as group_f:
    group = yaml.safe_load(group_f)

group["consulting_stats"]["num_consulting_sessions"] = 119

with open('data/group.yaml', 'w') as update_group_f:
    yaml.safe_dump(group, update_group_f, default_flow_style=False)

