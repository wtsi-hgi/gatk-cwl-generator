#!/bin/python

import os
import sys
import requests
from bs4 import BeautifulSoup

import json2cwl


def get_json_links(version):
    base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s-0/" % version
    data = requests.get(base_url).text
    soup = BeautifulSoup(data, "html.parser")
    tool_urls = []

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
    return [base_url, tool_urls]


def generate_cwl_and_json_files(out_dir, tool_urls, base_url):
    # Get current directory and make folders for files
    json_dir = os.path.join(out_dir, 'jsonfolder')
    cwl_dir = os.path.join(out_dir, 'cwlfiles')

    os.makedirs(json_dir)
    os.makedirs(cwl_dir)

    # Create json for each tool and convert to cwl
    for tool_url in tool_urls:
        os.chdir(json_dir)
        full_tool_url = base_url + tool_url
        tool_json = requests.get(full_tool_url)
        fname = tool_json.json()['name'] + '.json'
        
        print(fname)
        f = open(fname, 'w+')
        f.write(tool_json.text)
        f.close()

        json2cwl.make_cwl(json_dir, cwl_dir, fname)
        print("made cwl")

    print("success!!!!!!!!")


def main():
    # If two arguments are not given, use default arguments of v3.5 and output directory of ./cwlscripts
    if len(sys.argv) == 1:
        version = '3.5'
        out_dir = os.getcwd() + '/cwlscripts'
    else:
        version = sys.argv[1]
        out_dir = sys.argv[2]

    [base_url, tool_urls] = get_json_links(version)
    generate_cwl_and_json_files(out_dir, tool_urls, base_url)


if __name__ == '__main__':
    main()
