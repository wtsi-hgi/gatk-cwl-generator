#!/bin/python

import requests
import os
import json
import sys
from bs4 import BeautifulSoup
import pprint

# import json2cwl.py


def prepare_json_links(version):
    url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s-0/" %(version)
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    url_list = []
    for sub in soup.find_all('tr'):
        for child in sub.find_all('td'):
            for a in child.find_all('a', href = True):
                url_list.append(a['href'] + ".json") if "Exception" not in a['href'] else ''

    return url_list


url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/3.5-0/"

r = requests.get(url)
data = r.text

soup = BeautifulSoup(data, "html.parser")
#print(soup)

url_list = []

for sub in soup.find_all('tr'):
    for child in sub.find_all('td'):
        for a in child.find_all('a', href = True):
            url_list.append(a['href'] + ".json") if "Exception" not in a['href'] else ''

current = os.getcwd()
directory = os.path.join(current, 'jsonfolder')
os.makedirs(directory)
os.chdir(directory)

for tool in url_list:
    json_1 = url + tool
    r = requests.get(json_1).json()
    fname = r['name'] + '.json'
    f = open(fname, 'a')
    f.write(json.dumps(r, indent = 4, sort_keys = False))
    f.close()


# json_1 = url + url_list[0]

# r = requests.get(json_1)

# re = r.json()

# fname = re['name'] + '.json'
# f = open(fname, 'a')
# f.write(json.dumps(re, indent = 4, sort_keys = False))
# f.close()




# pprint.pprint(r.json())
# print(r.json()['arguments'][0]["defaultValue"])


# directory = sys.argv[1]
# version = sys.argv[2]

# dirFiles = os.listdir(directory)

