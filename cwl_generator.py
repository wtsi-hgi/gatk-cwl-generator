# converts GATK tools in .json to .cwl
from helper_functions import *

invalid_args = ['--input_file','--reference_sequence','--help', '--defaultBaseQualities']

def cwlf_generator(item,cwlf):
    comLine = ""       
    outputs = []
    inputs = [{ "doc": "fasta file of reference genome", "type": "File",
                 "id": "reference_sequence", "secondaryFiles": [".fai","^.dict"]},
               { "doc": "Index file of reference genome", "type": "File", "id": "refIndex"},
               { "doc": "dict file of reference genome", "type": "File", "id": "refDict"},
               { "doc": "Input file containing sequence data (BAM or CRAM)", "type": "File",
                 "id": "input_file","secondaryFiles": [".crai","^.dict"]}]      

    for args in item['arguments']:
      inpt = {}
      # if args['name'] in invalid_args:
      #   continue

      inpt['doc'] = args['summary']
      inpt['id'] = args['name'][2:] 
      type_writer(args,inpt)
      
      #input file, reference sequence
      
      #if inputfile:
      #secondaryFiles = ['.crai','^.dict']

#function secondary_files(f) { return typeof f; if (f.indexOf('.cram')!= -1 ){ return '.crai';} 
# else if (f.search('.bam')) { return '.bai'; } else if (f.search('.fa')) { return ['.fai','^.dict']; }}"""



      if 'requires' in args['fulltext'] and 'index' in args['fulltext']:
        print(args['name'])
         inpt['secondaryFiles'] = '$(secondary_files(self))'

      inputs.append(inpt)
      output_writer(args,outputs)
      comLine = commandline_writer(args,comLine)



    cwlf["inputs"] = inputs
    cwlf["outputs"] = outputs
    cwlf["arguments"] = [{"shellQuote": False,    
                          "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar  -R $(WDLCommandPart('NonNull(inputs.reference_sequence.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) " +  comLine}] 
                                          