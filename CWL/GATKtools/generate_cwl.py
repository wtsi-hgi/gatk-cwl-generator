#!/bin/python

import requests
import os
import json
import sys
from bs4 import BeautifulSoup
import pprint
import argparse
import shutil

import json2cwl

dev = True

def get_json_links(version):
    if type(version) == "current":
       base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s/" % version
   else:
       base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s-0/" % version
    data = requests.get(base_url).text
    soup = BeautifulSoup(data, "html.parser")
    tool_urls = []
    print('getting files from: ', base_url)    

    # Parse the html to obtain all json file links
    for link in soup.select("tr > td > a"):
        href = link['href']
        if href.startswith("org_broadinstitute_gatk") and "Exception" not in href:
            tool_urls.append(href + ".json")

    # Remove duplicates
    tool_urls = list(set(tool_urls))
    
    # Move CommandLine to the front of the list
    i = tool_urls.index("org_broadinstitute_gatk_engine_CommandLineGATK.php.json")
    tool_urls[0], tool_urls[i] = tool_urls[i], tool_urls[0]
    # print(url_list)
    return [base_url, tool_urls]


def generate_cwl_and_json_files(out_dir, tool_urls, base_url):
    print("creating and converting json files...")
    
    # Get current directory and make folders for files
    json_dir = os.path.join(out_dir, 'jsonfolder')
    cwl_dir = os.path.join(out_dir, 'cwlfiles')

    try:
        os.makedirs(json_dir)
        os.makedirs(cwl_dir)
    except OSError, e:
        if dev:
            shutil.rmtree(json_dir) # Removing existing generated files if the folder already exists, for testing
            shutil.rmtree(cwl_dir)
            os.makedirs(json_dir)
            os.makedirs(cwl_dir)
        else:
            raise e

    # Create json for each tool and convert to cwl
    for tool_url in tool_urls:
        full_tool_url = base_url + tool_url
        tool_json = requests.get(full_tool_url)
        tool_name = tool_json.json()['name']
        json_name = tool_name + ".json"

        f = open(os.path.join(json_dir, json_name), 'w+')
        f.write(tool_json.text)
        f.close()
        print("Written jsonfolder/" + json_name)

        json2cwl.make_cwl(json_dir, cwl_dir, json_name)
        print("Written cwlfiles/" + tool_name + ".cwl")

    print("Success!")


def main():
    #default version is 3.5-0
    #default directory is current directory/cwlscripts

    parser = argparse.ArgumentParser(description = 'take in GATK documentation version and specify output directory')
    parser.add_argument('-v', action='store', dest='gatkversion')
    parser.add_argument('-out', action='store', dest='outputdir')
    results = parser.parse_args()
        
    if results.gatkversion:
      version = results.gatkversion
    else:
      version = '3.5'
    
    if results.outputdir:
      directory = results.outputdir
    else:
      directory = os.getcwd() + '/cwlscripts'

    print("your chosen directory is: %s" % directory)
    url_list = get_json_links(version)
    generate_cwl_and_json_files(directory, url_list[1], url_list[0])


if __name__ == '__main__':
    main()
