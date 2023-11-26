# script to validate yaml file
# pip install pyyaml

import yaml

with open('YAML.yml', 'r') as file:
    try:
        print(yaml.safe_load(file))
    except yaml.YAMLError as exc:
        print(exc)


# OUTPUT
"""
{'name': 'Shiva', 'roll.no': 48, 
'server': {'name': 'server name', 'capacity': '50GB'}, 
'social_media': ['instagram', 'fb', 'x (former twitter)', 'YT'], 
'testing': 'this is\nmultiline\nstring\n', 
'list_of_servers': [{'server_1': None, 'name': 'ec2', 'vol': '8GB'}, {'server_2': None, 'name': 'fargate', 'vol': '10GB'}]}
"""