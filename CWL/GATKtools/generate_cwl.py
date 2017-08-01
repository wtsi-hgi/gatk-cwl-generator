#!/bin/python

import requests
import os
import json
import sys
from bs4 import BeautifulSoup
import pprint
import argparse

import json2cwl

parser = argparse.ArgumentParser(description = 'take in GATK documentation version and specify output directory')
parser.add_argument('-v',action='store',dest='gatkversion')
parser.add_argument('-out',action='store',dest='outputdir')
results = parser.parse_args()


def prepare_json_links(version):
    if type(version) == "current":
       url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s/" %(version)
    else:
       url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s-0/" %(version)
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    url_list = []
    print('getting files from: ',url)    

    ##parse the html to obtain all json file links
    for sub in soup.find_all('tr'):
        for child in sub.find_all('td'):
            for a in child.find_all('a', href = True):
                href = a['href']
                if href.startswith("org_broadinstitute_gatk") and "Exception" not in href:
                    url_list.append(href + ".json")

    ##remove duplicates
    url_list = list(set(url_list))
    
    ##move CommandLine to the front of the list
    i = url_list.index("org_broadinstitute_gatk_engine_CommandLineGATK.php.json")
    url_list[0], url_list[i] = url_list[i], url_list[0]
    # print(url_list)
    return [url, url_list]


def convert_json_files(fromdir, url_list, url):

    print("creating and converting json files...")
    
    ##get current directory and make folders for files
    directory = os.path.join(fromdir, 'jsonfolder')
    todir = os.path.join(fromdir, 'cwlfiles')
    os.makedirs(directory)
    os.makedirs(todir)

    #create json for each tool and conver to cwl
    for tool in url_list:
        #print(tool)
        os.chdir(directory)
        json_1 = url + tool
        r = requests.get(json_1)
        # r = requests.get(json_1).json()
        fname = r.json()['name'] + '.json'
#        print(fname)
        f = open(fname, 'w+')
        # f.write(json.dumps(r, indent = 4, sort_keys = False))
        f.write(r.text)
        f.close()
        json2cwl.make_cwl(directory, todir, fname)
#        print("made cwl")

    print("success!!!!!!!!")


def main():
    #default version is 3.5-0
    #default directory is current directory/cwlscripts
    
    if results.gatkversion:
      version = results.gatkversion
    else:
      version = '3.5'
    
    if results.outputdir:
      directory = results.outputdir
    else:
      directory = os.getcwd()+'/cwlscripts'

    print("your chosen directory is: %s" %(directory))
    url_list = prepare_json_links(version)
    convert_json_files(directory, url_list[1], url_list[0])


if __name__ == '__main__':
    main()
    
# current = os.getcwd()

# url_list = prepare_json_links(3.5)
# # print(url_list[1])
# convert_json_files(current, url_list[1], url_list[0])


# directory = sys.argv[1]
# version = sys.argv[2]

# dirFiles = os.listdir(directory)

