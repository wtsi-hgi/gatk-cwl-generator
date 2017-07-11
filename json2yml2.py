import json
import pyyaml


print9("hello")
f = open('HaplotypeCaller.cwl', 'r')
jsonData = json.load(f)
f.close()

print(jsonData)

yamlData = {}
yaml.dump(yamlData)

print(yamlData)
