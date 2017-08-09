#!/bin/python

import os
import argparse
import shutil
import itertools
import json

from bs4 import BeautifulSoup
import requests

import json2cwl

def find_index(lst, func):
    for i, item in enumerate(lst):
        if func(item):
            return i
    
    raise ValueError("Item not found")

class JSONLinks:
    def __init__(self, tool_urls, annotator_urls, readfilter_urls, resourcefile_urls):
        self.tool_urls = tool_urls
        self.annotator_urls = annotator_urls
        self.readfilter_urls = readfilter_urls
        self.resourcefile_urls = resourcefile_urls

def get_json_links(version):
    """
    Parses the tool docs HTML page to get links to the json resources
    """
    if version == "current" or version.startswith("4"):
       base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s/" % version
    else:
       base_url = "https://software.broadinstitute.org/gatk/documentation/tooldocs/%s-0/" % version
    
    data = requests.get(base_url).text
    soup = BeautifulSoup(data, "html.parser")

    tool_urls = []

    annotator_urls = []
    readfile_urls = []
    resourcefile_urls = []

    starting_str = "org_broadinstitute_gatk" if is_version_3(version) else "org_broadinstitute_hellbender"

    # Parse the html to obtain all json file links
    for link in soup.select("tr > td > a"):
        href = link['href']
        if href.startswith(starting_str) and "Exception" not in href:
            full_url = base_url + href + ".json"
            rest_text = href[len(starting_str + "_"):]

            # Need to process these separately
            if rest_text.startswith("tools_walkers_annotator") \
                    and "VariantAnnotator" not in rest_text:
                    # VariantAnnotator is wrongly categorized in it's url (it's a tool)
                annotator_urls.append(full_url)
            elif rest_text.startswith("engine_filters"):
                readfile_urls.append(full_url)
            elif rest_text.startswith("utils_codecs"):
                resourcefile_urls.append(full_url)
            else:
                tool_urls.append(full_url)

    # Remove duplicates
    tool_urls = list(set(tool_urls))
    
    # Move CommandLine to the front of the list
    if is_version_3(version):
        i = find_index(tool_urls, lambda x: "CommandLineGATK" in x)
        tool_urls[0], tool_urls[i] = tool_urls[i], tool_urls[0]

    return JSONLinks(tool_urls, annotator_urls, readfile_urls, resourcefile_urls)


def is_version_3(version):
    return not version.startswith("4")

def generate_cwl_and_json_files(out_dir, grouped_urls, cmd_line_options):
    """
    Generates the cwl and json files
    """
    global_args = get_global_arguments(grouped_urls, is_version_3(cmd_line_options.gatkversion))

    print("Creating and converting json files...")
    
    # Get current directory and make folders for files
    json_dir = os.path.join(out_dir, 'json')
    cwl_dir = os.path.join(out_dir, 'cwl')

    try:
        os.makedirs(json_dir)
        os.makedirs(cwl_dir)
    except OSError as e:
        if cmd_line_options.dev:
            shutil.rmtree(json_dir) # Removing existing generated files if the folder already exists, for testing
            shutil.rmtree(cwl_dir)
            os.makedirs(json_dir)
            os.makedirs(cwl_dir)
        else:
            raise e


    # Create json for each tool and convert to cwl
    for tool_url in grouped_urls.tool_urls:
        if cmd_line_options.include_file is None or cmd_line_options.include_file in tool_url or "CommandLineGATK" in tool_url:
            tool_json = requests.get(tool_url)
            
            tool_json_json = tool_json.json()
            tool_name = tool_json_json['name']
            json_name = tool_name + ".json"
            
            f = open(os.path.join(json_dir, json_name), 'w+')
            f.write(tool_json.text)
            f.close()
            print("Written json/" + json_name)

            # Don't append options for CommandLinkGATK or read filters for CatVariants,
            # it bypasses the GATK engine
            # https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_gatk_tools_CatVariants.php
            if not (tool_name == "CommandLineGATK" or tool_name == "CatVariants"):
                apply_global_arguments(tool_json_json, global_args)

            json2cwl.json2cwl(
                tool_json_json,
                cwl_dir,
                cmd_line_options
            )
            print("Written cwl/" + tool_name + ".cwl")

    print("Success!")

def apply_global_arguments(GATK_json, global_args):
    """
    Adds globals arguments to the GATK json object, not adding arguments if they are duplicated
    in the GATK json file

    :param GATK_json: The GATK json object to modify
    :param global_args: An array of arguments to add as global arguments
    """
    GATK_args_names = set(arg["name"] for arg in GATK_json["arguments"])

    for global_arg in global_args:
        if global_arg["name"] not in GATK_args_names:
            GATK_json["arguments"].append(global_arg)

def get_global_arguments(grouped_urls, apply_cmdlineGATK):
    """
    Get arguments (e.g. CommandLinkGATK and read filters) that should be avaliable to all CWL files

    :param grouped_urls: Urls as generated by get_json_links
    :param apply_cmdlineGATK: should be false on v4+
    """
    arguments = []

    if apply_cmdlineGATK:
        commandLineGATK = requests.get(grouped_urls.tool_urls[0]).json() # This should be CommandLinkGATK
        arguments.extend(commandLineGATK["arguments"])

    print("Getting read filter arguments ...")

    for readfilter_url in grouped_urls.readfilter_urls:
        readfilter_json = requests.get(readfilter_url).json()
        print("Fetched " + readfilter_url)
        
        if "arguments" in readfilter_json:
            args = readfilter_json["arguments"]

            for arg in args:
                arg["defaultValue"] = "NA" # This argument is not necessarily valid, so we shouldn't set the default
                arg["required"] = "no"

            arguments.extend(args)
    return arguments

def main():
    parser = argparse.ArgumentParser(description='Generates CWL files from the GATK documentation')
    parser.add_argument("--version", "-v", dest='gatkversion', default="3.5",
        help="Sets the version of GATK to parse documentation for. Default is 3.5")
    parser.add_argument('--out', "-o", dest='outputdir',
        help="Sets the output directory for generated files. Default is ./cwl_files_<VERSION>")
    parser.add_argument('--include', dest='include_file',
        help="Only generate this file (note, CommandLinkGATK has to be generated for v3.x)")
    parser.add_argument("--dev", dest="dev", action="store_true",
        help="Enable network caching and overwriting of the generated files (for development purposes)")
    parser.add_argument("--docker_container_name", "-c", dest="docker_container_name", default="gatk",
        help="Enable network caching and overwriting of the generated files (for development purposes). " + 
        "Default is 'gatk'")
    cmd_line_options = parser.parse_args()


    if cmd_line_options.dev:
        import requests_cache
        requests_cache.install_cache() # Decreases the time to run dramatically
    
    if not cmd_line_options.outputdir:
      cmd_line_options.outputdir = os.getcwd() + '/cwl_files_%s' % cmd_line_options.gatkversion

    print("Your chosen directory is: %s" % cmd_line_options.outputdir)
    grouped_urls = get_json_links(cmd_line_options.gatkversion)

    generate_cwl_and_json_files(cmd_line_options.outputdir, grouped_urls, cmd_line_options)


if __name__ == '__main__':
    main()
