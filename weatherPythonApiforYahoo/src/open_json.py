import json
from pprint import pprint

json_data=open("example.json").read()

data = json.loads(json_data)
pprint(data)
