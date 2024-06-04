# read group.yaml
# update to new values
# dump group.yaml

import yaml
from pprint import pprint

with open('data/group.yaml') as group_f:
    group = yaml.safe_load(group_f)

pprint(group["consulting_stats"])