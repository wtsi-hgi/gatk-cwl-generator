{
    "inputs": [
        {
            "id": "ref",
            "type": "File",
            "doc": "fasta file of reference genome",
            "secondaryFiles": [
                ".fai",
                "^.dict"
            ]
        },
        {
            "id": "refIndex",
            "type": "File",
            "doc": "Index file of reference genome"
        },
        {
            "id": "refDict",
            "type": "File",
            "doc": "dict file of reference genome"
        },
        {
            "id": "input_file",
            "type": "File",
            "doc": "Input file containing sequence data (BAM or CRAM)",
            "secondaryFiles": [
                ".crai"
            ]
        },
        {
            "id": "activeProbabilityThreshold",
            "type": "float?",
            "doc": "Threshold for the probability of a profile state being active."
        },
        {
            "id": "activeRegionExtension",
            "type": "int?",
            "doc": "The active region extension; if not provided defaults to Walker annotated default"
        },
        {
            "id": "activeRegionIn",
            "type": "string[]?",
            "doc": "Use this interval list file as the active regions to process"
        },
        {
            "id": "activeRegionMaxSize",
            "type": "int?",
            "doc": "The active region maximum size; if not provided defaults to Walker annotated default"
        },
        {
            "id": "activeRegionOut",
            "type": "string?",
            "doc": "Output the active region to this IGV formatted file"
        },
        {
            "id": "activityProfileOut",
            "type": "string?",
            "doc": "Output the raw activity profile results in IGV format"
        },
        {
            "id": "alleles",
            "type": "string?",
            "doc": "Set of alleles to use in genotyping"
        },
        {
            "id": "allowNonUniqueKmersInRef",
            "type": "boolean?",
            "doc": "Allow graphs that have non-unique kmers in the reference"
        },
        {
            "id": "allSitePLs",
            "type": "boolean?",
            "doc": "Annotate all sites with PLs"
        },
        {
            "id": "annotateNDA",
            "type": "boolean?",
            "doc": "Annotate number of alleles observed"
        },
        {
            "id": "annotation",
            "type": "string[]?",
            "doc": "One or more specific annotations to apply to variant calls"
        },
        {
            "id": "bamOutput",
            "type": "string?",
            "doc": "File to which assembled haplotypes should be written"
        },
        {
            "id": "bamWriterType",
            "type": "string?",
            "doc": "Which haplotypes should be written to the BAM"
        },
        {
            "id": "bandPassSigma",
            "type": "float?",
            "doc": "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default"
        },
        {
            "id": "comp",
            "type": "string[]?",
            "doc": "Comparison VCF file"
        },
        {
            "id": "consensus",
            "type": "boolean?",
            "doc": "1000G consensus mode"
        },
        {
            "id": "contamination_fraction_per_sample_file",
            "type": "File?",
            "doc": "Contamination per sample"
        },
        {
            "id": "contamination_fraction_to_filter",
            "type": "float?",
            "doc": "Fraction of contamination to aggressively remove"
        },
        {
            "id": "dbsnp",
            "type": "string?",
            "doc": "dbSNP file"
        },
        {
            "id": "debug",
            "type": "boolean?",
            "doc": "Print out very verbose debug information about each triggering active region"
        },
        {
            "id": "disableOptimizations",
            "type": "boolean?",
            "doc": "Don't skip calculations in ActiveRegions with no variants"
        },
        {
            "id": "doNotRunPhysicalPhasing",
            "type": "boolean?",
            "doc": "Disable physical phasing"
        },
        {
            "id": "dontIncreaseKmerSizesForCycles",
            "type": "boolean?",
            "doc": "Disable iterating over kmer sizes when graph cycles are detected"
        },
        {
            "id": "dontTrimActiveRegions",
            "type": "boolean?",
            "doc": "If specified, we will not trim down the active region from the full region (active + extension) to just the active interval for genotyping"
        },
        {
            "id": "dontUseSoftClippedBases",
            "type": "boolean?",
            "doc": "Do not analyze soft clipped bases in the reads"
        },
        {
            "id": "emitDroppedReads",
            "type": "boolean?",
            "doc": "Emit reads that are dropped for filtering, trimming, realignment failure"
        },
        {
            "id": "emitRefConfidence",
            "type": "string?",
            "doc": "Mode for emitting reference confidence scores"
        },
        {
            "id": "excludeAnnotation",
            "type": "string[]?",
            "doc": "One or more specific annotations to exclude"
        },
        {
            "id": "forceActive",
            "type": "boolean?",
            "doc": "If provided, all bases will be tagged as active"
        },
        {
            "id": "gcpHMM",
            "type": "string?",
            "doc": "Flat gap continuation penalty for use in the Pair HMM"
        },
        {
            "id": "genotyping_mode",
            "type": "string?",
            "doc": "Specifies how to determine the alternate alleles to use for genotyping"
        },
        {
            "id": "graphOutput",
            "type": "string?",
            "doc": "Write debug assembly graph information to this file"
        },
        {
            "id": "group",
            "type": "string[]?",
            "doc": "One or more classes/groups of annotations to apply to variant calls"
        },
        {
            "id": "GVCFGQBands",
            "type": "int[]?",
            "doc": "Exclusive upper bounds for reference confidence GQ bands (must be in [1, 100] and specified in increasing order)"
        },
        {
            "id": "heterozygosity",
            "type": "float?",
            "doc": "Heterozygosity value used to compute prior likelihoods for any locus"
        },
        {
            "id": "heterozygosity_stdev",
            "type": "float?",
            "doc": "Standard deviation of eterozygosity for SNP and indel calling."
        },
        {
            "id": "indel_heterozygosity",
            "type": "float?",
            "doc": "Heterozygosity for indel calling"
        },
        {
            "id": "indelSizeToEliminateInRefModel",
            "type": "string?",
            "doc": "The size of an indel to check for in the reference model"
        },
        {
            "id": "input_prior",
            "type": "float[]?",
            "doc": "Input prior for calls"
        },
        {
            "id": "kmerSize",
            "type": "int[]?",
            "doc": "Kmer size to use in the read threading assembler"
        },
        {
            "id": "max_alternate_alleles",
            "type": "string?",
            "doc": "Maximum number of alternate alleles to genotype"
        },
        {
            "id": "max_genotype_count",
            "type": "string?",
            "doc": "Maximum number of genotypes to consider at any site"
        },
        {
            "id": "max_num_PL_values",
            "type": "string?",
            "doc": "Maximum number of PL values to output"
        },
        {
            "id": "maxNumHaplotypesInPopulation",
            "type": "string?",
            "doc": "Maximum number of haplotypes to consider for your population"
        },
        {
            "id": "maxReadsInMemoryPerSample",
            "type": "string?",
            "doc": "Maximum reads per sample given to traversal map() function"
        },
        {
            "id": "maxReadsInRegionPerSample",
            "type": "string?",
            "doc": "Maximum reads in an active region"
        },
        {
            "id": "maxTotalReadsInMemory",
            "type": "string?",
            "doc": "Maximum total reads given to traversal map() function"
        },
        {
            "id": "min_base_quality_score",
            "type": "string?",
            "doc": "Minimum base quality required to consider a base for calling"
        },
        {
            "id": "minDanglingBranchLength",
            "type": "string?",
            "doc": "Minimum length of a dangling branch to attempt recovery"
        },
        {
            "id": "minPruning",
            "type": "string?",
            "doc": "Minimum support to not prune paths in the graph"
        },
        {
            "id": "minReadsPerAlignmentStart",
            "type": "string?",
            "doc": "Minimum number of reads sharing the same alignment start for each genomic location in an active region"
        },
        {
            "id": "numPruningSamples",
            "type": "string?",
            "doc": "Number of samples that must pass the minPruning threshold"
        },
        {
            "id": "out",
            "type": "string?",
            "doc": "File to which variants should be written"
        },
        {
            "id": "output_mode",
            "type": "string?",
            "doc": "Which type of calls we should output"
        },
        {
            "id": "pcr_indel_model",
            "type": "string?",
            "doc": "The PCR indel model to use"
        },
        {
            "id": "phredScaledGlobalReadMismappingRate",
            "type": "string?",
            "doc": "The global assumed mismapping rate for reads"
        },
        {
            "id": "sample_name",
            "type": "string?",
            "doc": "Name of single sample to use from a multi-sample bam"
        },
        {
            "id": "sample_ploidy",
            "type": "string?",
            "doc": "Ploidy per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy)."
        },
        {
            "id": "standard_min_confidence_threshold_for_calling",
            "type": "float?",
            "doc": "The minimum phred-scaled confidence threshold at which variants should be called"
        },
        {
            "id": "useAllelesTrigger",
            "type": "boolean?",
            "doc": "Use additional trigger on variants found in an external alleles file"
        },
        {
            "id": "useFilteredReadsForAnnotations",
            "type": "boolean?",
            "doc": "Use the contamination-filtered read maps for the purposes of annotating variants"
        },
        {
            "id": "useNewAFCalculator",
            "type": "boolean?",
            "doc": "Use new AF model instead of the so-called exact model"
        }
    ],
    "requirements": [
        {
            "class": "ShellCommandRequirement"
        },
        {
            "expressionLib": [
                "function WDLCommandPart(expr, def) {var rval; try {rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                "function NonNull(x) {if(x === null) {throw new UserException('NullValue');} else {return x;}}",
                "function defHandler(com, def) {if(Array.isArray(def) && def.length == 0) {return '';} else if(Array.isArray(def) && def.length !=0 ) {return def.map(elementh=> com+ ' ' + element).join(' ');} else if (def =='false') {return '';} else if (def == 'true') {return com;} if (def == []) {return '';} else {return com + def;}}"
            ],
            "class": "InlineJavascriptRequirement"
        },
        {
            "dockerPull": "gatk:latest",
            "class": "DockerRequirement"
        }
    ],
    "id": "HaplotypeCaller",
    "arguments": [
        {
            "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', ''))  $(defHandler('-ActProbThresh', WDLCommandPart('NonNull(inputs.activeProbabilityThreshold)', '0.002')))  $(defHandler('-activeRegionExtension', WDLCommandPart('NonNull(inputs.activeRegionExtension)', ' ')))  $(defHandler('-AR', WDLCommandPart('NonNull(inputs.activeRegionIn)', ' ')))  $(defHandler('-activeRegionMaxSize', WDLCommandPart('NonNull(inputs.activeRegionMaxSize)', ' ')))  $(defHandler('-ARO', WDLCommandPart('NonNull(inputs.activeRegionOut)', ' ')))  $(defHandler('-APO', WDLCommandPart('NonNull(inputs.activityProfileOut)', ' ')))  $(defHandler('-alleles', WDLCommandPart('NonNull(inputs.alleles)', 'none')))  $(defHandler('-allowNonUniqueKmersInRef', WDLCommandPart('NonNull(inputs.allowNonUniqueKmersInRef)', 'false')))  $(defHandler('-allSitePLs', WDLCommandPart('NonNull(inputs.allSitePLs)', 'false')))  $(defHandler('-nda', WDLCommandPart('NonNull(inputs.annotateNDA)', 'false')))  $(defHandler('-A', WDLCommandPart('NonNull(inputs.annotation)', '[]')))  $(defHandler('-bamout', WDLCommandPart('NonNull(inputs.bamOutput)', ' ')))  $(defHandler('-bamWriterType', WDLCommandPart('NonNull(inputs.bamWriterType)', 'CALLED_HAPLOTYPES')))  $(defHandler('-bandPassSigma', WDLCommandPart('NonNull(inputs.bandPassSigma)', ' ')))  $(defHandler('-comp', WDLCommandPart('NonNull(inputs.comp)', '[]')))  $(defHandler('-consensus', WDLCommandPart('NonNull(inputs.consensus)', 'false')))  $(defHandler('-contaminationFile', WDLCommandPart('NonNull(inputs.contamination_fraction_per_sample_file)', ' ')))  $(defHandler('-contamination', WDLCommandPart('NonNull(inputs.contamination_fraction_to_filter)', '0.0')))  $(defHandler('-D', WDLCommandPart('NonNull(inputs.dbsnp)', 'none')))  $(defHandler('-debug', WDLCommandPart('NonNull(inputs.debug)', 'false')))  $(defHandler('-disableOptimizations', WDLCommandPart('NonNull(inputs.disableOptimizations)', 'false')))  $(defHandler('-doNotRunPhysicalPhasing', WDLCommandPart('NonNull(inputs.doNotRunPhysicalPhasing)', 'false')))  $(defHandler('-dontIncreaseKmerSizesForCycles', WDLCommandPart('NonNull(inputs.dontIncreaseKmerSizesForCycles)', 'false')))  $(defHandler('-dontTrimActiveRegions', WDLCommandPart('NonNull(inputs.dontTrimActiveRegions)', 'false')))  $(defHandler('-dontUseSoftClippedBases', WDLCommandPart('NonNull(inputs.dontUseSoftClippedBases)', 'false')))  $(defHandler('-edr', WDLCommandPart('NonNull(inputs.emitDroppedReads)', 'false')))  $(defHandler('-ERC', WDLCommandPart('NonNull(inputs.emitRefConfidence)', 'false')))  $(defHandler('-XA', WDLCommandPart('NonNull(inputs.excludeAnnotation)', '[]')))  $(defHandler('-forceActive', WDLCommandPart('NonNull(inputs.forceActive)', 'false')))  $(defHandler('-gcpHMM', WDLCommandPart('NonNull(inputs.gcpHMM)', '10')))  $(defHandler('-gt_mode', WDLCommandPart('NonNull(inputs.genotyping_mode)', 'DISCOVERY')))  $(defHandler('-graph', WDLCommandPart('NonNull(inputs.graphOutput)', ' ')))  $(defHandler('-G', WDLCommandPart('NonNull(inputs.group)', '[StandardAnnotation, StandardHCAnnotation]')))  $(defHandler('-GQB', WDLCommandPart('NonNull(inputs.GVCFGQBands)', '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 70, 80, 90, 99]')))  $(defHandler('-hets', WDLCommandPart('NonNull(inputs.heterozygosity)', '0.001')))  $(defHandler('-heterozygosityStandardDeviation', WDLCommandPart('NonNull(inputs.heterozygosity_stdev)', '0.01')))  $(defHandler('-indelHeterozygosity', WDLCommandPart('NonNull(inputs.indel_heterozygosity)', '1.25E-4')))  $(defHandler('-ERCIS', WDLCommandPart('NonNull(inputs.indelSizeToEliminateInRefModel)', '10')))  $(defHandler('-inputPrior', WDLCommandPart('NonNull(inputs.input_prior)', '[]')))  $(defHandler('-kmerSize', WDLCommandPart('NonNull(inputs.kmerSize)', '[10, 25]')))  $(defHandler('-maxAltAlleles', WDLCommandPart('NonNull(inputs.max_alternate_alleles)', '6')))  $(defHandler('-maxGT', WDLCommandPart('NonNull(inputs.max_genotype_count)', '1024')))  $(defHandler('-maxNumPLValues', WDLCommandPart('NonNull(inputs.max_num_PL_values)', '100')))  $(defHandler('-maxNumHaplotypesInPopulation', WDLCommandPart('NonNull(inputs.maxNumHaplotypesInPopulation)', '128')))  $(defHandler('-maxReadsInMemoryPerSample', WDLCommandPart('NonNull(inputs.maxReadsInMemoryPerSample)', '30000')))  $(defHandler('-maxReadsInRegionPerSample', WDLCommandPart('NonNull(inputs.maxReadsInRegionPerSample)', '10000')))  $(defHandler('-maxTotalReadsInMemory', WDLCommandPart('NonNull(inputs.maxTotalReadsInMemory)', '10000000')))  $(defHandler('-mbq', WDLCommandPart('NonNull(inputs.min_base_quality_score)', '10')))  $(defHandler('-minDanglingBranchLength', WDLCommandPart('NonNull(inputs.minDanglingBranchLength)', '4')))  $(defHandler('-minPruning', WDLCommandPart('NonNull(inputs.minPruning)', '2')))  $(defHandler('-minReadsPerAlignStart', WDLCommandPart('NonNull(inputs.minReadsPerAlignmentStart)', '10')))  $(defHandler('-numPruningSamples', WDLCommandPart('NonNull(inputs.numPruningSamples)', '1')))  $(defHandler('-o', WDLCommandPart('NonNull(inputs.out)', 'stdout')))  $(defHandler('-out_mode', WDLCommandPart('NonNull(inputs.output_mode)', 'EMIT_VARIANTS_ONLY')))  $(defHandler('-pcrModel', WDLCommandPart('NonNull(inputs.pcr_indel_model)', 'CONSERVATIVE')))  $(defHandler('-globalMAPQ', WDLCommandPart('NonNull(inputs.phredScaledGlobalReadMismappingRate)', '45')))  $(defHandler('-sn', WDLCommandPart('NonNull(inputs.sample_name)', ' ')))  $(defHandler('-ploidy', WDLCommandPart('NonNull(inputs.sample_ploidy)', '2')))  $(defHandler('-stand_call_conf', WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_calling)', '10.0')))  $(defHandler('-allelesTrigger', WDLCommandPart('NonNull(inputs.useAllelesTrigger)', 'false')))  $(defHandler('-useFilteredReadsForAnnotations', WDLCommandPart('NonNull(inputs.useFilteredReadsForAnnotations)', 'false')))  $(defHandler('-newQual', WDLCommandPart('NonNull(inputs.useNewAFCalculator)', 'false')))",
            "shellQuote": false
        }
    ],
    "cwlVersion": "v1.0",
    "baseCommand": [],
    "outputs": [
        {
            "outputBinding": {
                "glob": "$(inputs.out)"
            },
            "type": "File",
            "id": "taskOut"
        }
    ],
    "class": "CommandLineTool"
}