#!/bin/python

import os
import sys
import requests
from bs4 import BeautifulSoup

import json2cwl


def prepare_json_links(version):
    url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s-0/" % version
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    url_list = []

    # Parse the html to obtain all json file links
    for sub in soup.find_all('tr'):
        for child in sub.find_all('td'):
            for a in child.find_all('a', href = True):
                href = a['href']
                if href.startswith("org_broadinstitute_gatk") and "Exception" not in href:
                    url_list.append(href + ".json")

    # Remove duplicates
    url_list = list(set(url_list))
    
    # Move CommandLine to the front of the list
    i = url_list.index("org_broadinstitute_gatk_engine_CommandLineGATK.php.json")
    url_list[0], url_list[i] = url_list[i], url_list[0]
    return [url, url_list]


def convert_json_files(fromdir, url_list, url):
    print("creating and converting json files...")
    
    # Get current directory and make folders for files
    directory = os.path.join(fromdir, 'jsonfolder')
    todir = os.path.join(fromdir, 'cwlfiles')
    os.makedirs(directory)
    os.makedirs(todir)

    # Create json for each tool and conver to cwl
    for tool in url_list:
        os.chdir(directory)
        json_1 = url + tool
        r = requests.get(json_1)
        fname = r.json()['name'] + '.json'
        print(fname)
        f = open(fname, 'w+')
        f.write(r.text)
        f.close()
        json2cwl.make_cwl(directory, todir, fname)
        print("made cwl")

    print("success!!!!!!!!")


def main():
    try:
      version = sys.argv[1]
      directory = sys.argv[2]
    except:
      version = '3.5'
      directory = os.getcwd()+'/cwlscripts'
    # Default version is 3.5-0
    # Default directory is current directory/cwlscripts

    url_list = prepare_json_links(version)
    convert_json_files(directory, url_list[1], url_list[0])


if __name__ == '__main__':
    main()
