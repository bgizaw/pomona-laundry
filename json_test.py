import json

f = open('templates/machineInfo.json')

data = json.load(f)
print(data[0]['dryers'])