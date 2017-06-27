{
    "requirements": [
        {
            "class": "ShellCommandRequirement"
        },
        {
            "expressionLib": [
                "function WDLCommandPart(expr, def) {var rval; try {rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                "function NonNull(x) {if(x === null) {throw new UserException(\"NullValue\");} else {return x;}}",
                "function defHandler(com, def) {if(Array.isArray(def) && def.length == 0) {return '';} else if(Array.isArray(def) && def.length !=0 ) {return def.map(elementh=> com+ ' ' + element).join(' ');} else if (def ==\"false\" {return ;} else if (def == \"true\" (return com;} if (def == []) {return ;} else {return com + def;}}"
            ],
            "class": "InlineJavascriptRequirement"
        },
        {
            "dockerPull": "gatk:latest",
            "class": "DockerRequirement"
        }
    ],
    "cwlVersion": "v1.0",
    "outputs": [
        {
            "id": "taskOut",
            "type": "File",
            "outputBinding": {
                "glob": "$(inputs.out)"
            }
        }
    ],
    "inputs": [
        {
            "id": "ref",
            "secondaryFiles": [
                ".fai",
                "^.dict"
            ],
            "doc": "fasta file of reference genome",
            "type": "File"
        },
        {
            "id": "refIndex",
            "doc": "Index file of reference genome",
            "type": "File"
        },
        {
            "id": "refDict",
            "doc": "dict file of reference genome",
            "type": "File"
        },
        {
            "id": "input_file",
            "secondaryFiles": [
                ".crai"
            ],
            "doc": "Input file containing sequence data (BAM or CRAM)",
            "type": "File"
        },
        {
            "id": "activeProbabilityThreshold",
            "doc": "Threshold for the probability of a profile state being active.",
            "type": "float?"
        },
        {
            "id": "activeRegionExtension",
            "doc": "The active region extension; if not provided defaults to Walker annotated default",
            "type": "int?"
        },
        {
            "id": "activeRegionIn",
            "doc": "Use this interval list file as the active regions to process",
            "type": "string[]?"
        },
        {
            "id": "activeRegionMaxSize",
            "doc": "The active region maximum size; if not provided defaults to Walker annotated default",
            "type": "int?"
        },
        {
            "id": "activeRegionOut",
            "doc": "Output the active region to this IGV formatted file",
            "type": "string?"
        },
        {
            "id": "activityProfileOut",
            "doc": "Output the raw activity profile results in IGV format",
            "type": "string?"
        },
        {
            "id": "alleles",
            "doc": "Set of alleles to use in genotyping",
            "type": "string?"
        },
        {
            "id": "allowNonUniqueKmersInRef",
            "doc": "Allow graphs that have non-unique kmers in the reference",
            "type": "boolean?"
        },
        {
            "id": "allSitePLs",
            "doc": "Annotate all sites with PLs",
            "type": "boolean?"
        },
        {
            "id": "annotateNDA",
            "doc": "Annotate number of alleles observed",
            "type": "boolean?"
        },
        {
            "id": "annotation",
            "doc": "One or more specific annotations to apply to variant calls",
            "type": "string[]?"
        },
        {
            "id": "bamOutput",
            "doc": "File to which assembled haplotypes should be written",
            "type": "string?"
        },
        {
            "id": "bamWriterType",
            "doc": "Which haplotypes should be written to the BAM",
            "type": "string?"
        },
        {
            "id": "bandPassSigma",
            "doc": "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default",
            "type": "float?"
        },
        {
            "id": "comp",
            "doc": "Comparison VCF file",
            "type": "string[]?"
        },
        {
            "id": "consensus",
            "doc": "1000G consensus mode",
            "type": "boolean?"
        },
        {
            "id": "contamination_fraction_per_sample_file",
            "doc": "Contamination per sample",
            "type": "File?"
        },
        {
            "id": "contamination_fraction_to_filter",
            "doc": "Fraction of contamination to aggressively remove",
            "type": "float?"
        },
        {
            "id": "dbsnp",
            "doc": "dbSNP file",
            "type": "string?"
        },
        {
            "id": "debug",
            "doc": "Print out very verbose debug information about each triggering active region",
            "type": "boolean?"
        },
        {
            "id": "disableOptimizations",
            "doc": "Don't skip calculations in ActiveRegions with no variants",
            "type": "boolean?"
        },
        {
            "id": "doNotRunPhysicalPhasing",
            "doc": "Disable physical phasing",
            "type": "boolean?"
        },
        {
            "id": "dontIncreaseKmerSizesForCycles",
            "doc": "Disable iterating over kmer sizes when graph cycles are detected",
            "type": "boolean?"
        },
        {
            "id": "dontTrimActiveRegions",
            "doc": "If specified, we will not trim down the active region from the full region (active + extension) to just the active interval for genotyping",
            "type": "boolean?"
        },
        {
            "id": "dontUseSoftClippedBases",
            "doc": "Do not analyze soft clipped bases in the reads",
            "type": "boolean?"
        },
        {
            "id": "emitDroppedReads",
            "doc": "Emit reads that are dropped for filtering, trimming, realignment failure",
            "type": "boolean?"
        },
        {
            "id": "emitRefConfidence",
            "doc": "Mode for emitting reference confidence scores",
            "type": "string?"
        },
        {
            "id": "excludeAnnotation",
            "doc": "One or more specific annotations to exclude",
            "type": "string[]?"
        },
        {
            "id": "forceActive",
            "doc": "If provided, all bases will be tagged as active",
            "type": "boolean?"
        },
        {
            "id": "gcpHMM",
            "doc": "Flat gap continuation penalty for use in the Pair HMM",
            "type": "string?"
        },
        {
            "id": "genotyping_mode",
            "doc": "Specifies how to determine the alternate alleles to use for genotyping",
            "type": "string?"
        },
        {
            "id": "graphOutput",
            "doc": "Write debug assembly graph information to this file",
            "type": "string?"
        },
        {
            "id": "group",
            "doc": "One or more classes/groups of annotations to apply to variant calls",
            "type": "string[]?"
        },
        {
            "id": "GVCFGQBands",
            "doc": "Exclusive upper bounds for reference confidence GQ bands (must be in [1, 100] and specified in increasing order)",
            "type": "int[]?"
        },
        {
            "id": "heterozygosity",
            "doc": "Heterozygosity value used to compute prior likelihoods for any locus",
            "type": "float?"
        },
        {
            "id": "heterozygosity_stdev",
            "doc": "Standard deviation of eterozygosity for SNP and indel calling.",
            "type": "float?"
        },
        {
            "id": "indel_heterozygosity",
            "doc": "Heterozygosity for indel calling",
            "type": "float?"
        },
        {
            "id": "indelSizeToEliminateInRefModel",
            "doc": "The size of an indel to check for in the reference model",
            "type": "string?"
        },
        {
            "id": "input_prior",
            "doc": "Input prior for calls",
            "type": "float[]?"
        },
        {
            "id": "kmerSize",
            "doc": "Kmer size to use in the read threading assembler",
            "type": "int[]?"
        },
        {
            "id": "max_alternate_alleles",
            "doc": "Maximum number of alternate alleles to genotype",
            "type": "string?"
        },
        {
            "id": "max_genotype_count",
            "doc": "Maximum number of genotypes to consider at any site",
            "type": "string?"
        },
        {
            "id": "max_num_PL_values",
            "doc": "Maximum number of PL values to output",
            "type": "string?"
        },
        {
            "id": "maxNumHaplotypesInPopulation",
            "doc": "Maximum number of haplotypes to consider for your population",
            "type": "string?"
        },
        {
            "id": "maxReadsInMemoryPerSample",
            "doc": "Maximum reads per sample given to traversal map() function",
            "type": "string?"
        },
        {
            "id": "maxReadsInRegionPerSample",
            "doc": "Maximum reads in an active region",
            "type": "string?"
        },
        {
            "id": "maxTotalReadsInMemory",
            "doc": "Maximum total reads given to traversal map() function",
            "type": "string?"
        },
        {
            "id": "min_base_quality_score",
            "doc": "Minimum base quality required to consider a base for calling",
            "type": "string?"
        },
        {
            "id": "minDanglingBranchLength",
            "doc": "Minimum length of a dangling branch to attempt recovery",
            "type": "string?"
        },
        {
            "id": "minPruning",
            "doc": "Minimum support to not prune paths in the graph",
            "type": "string?"
        },
        {
            "id": "minReadsPerAlignmentStart",
            "doc": "Minimum number of reads sharing the same alignment start for each genomic location in an active region",
            "type": "string?"
        },
        {
            "id": "numPruningSamples",
            "doc": "Number of samples that must pass the minPruning threshold",
            "type": "string?"
        },
        {
            "id": "out",
            "doc": "File to which variants should be written",
            "type": "string?"
        },
        {
            "id": "output_mode",
            "doc": "Which type of calls we should output",
            "type": "string?"
        },
        {
            "id": "pcr_indel_model",
            "doc": "The PCR indel model to use",
            "type": "string?"
        },
        {
            "id": "phredScaledGlobalReadMismappingRate",
            "doc": "The global assumed mismapping rate for reads",
            "type": "string?"
        },
        {
            "id": "sample_name",
            "doc": "Name of single sample to use from a multi-sample bam",
            "type": "string?"
        },
        {
            "id": "sample_ploidy",
            "doc": "Ploidy per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy).",
            "type": "string?"
        },
        {
            "id": "standard_min_confidence_threshold_for_calling",
            "doc": "The minimum phred-scaled confidence threshold at which variants should be called",
            "type": "float?"
        },
        {
            "id": "useAllelesTrigger",
            "doc": "Use additional trigger on variants found in an external alleles file",
            "type": "boolean?"
        },
        {
            "id": "useFilteredReadsForAnnotations",
            "doc": "Use the contamination-filtered read maps for the purposes of annotating variants",
            "type": "boolean?"
        },
        {
            "id": "useNewAFCalculator",
            "doc": "Use new AF model instead of the so-called exact model",
            "type": "boolean?"
        }
    ],
    "id": "HaplotypeCaller",
    "class": "CommandLineTool",
    "arguments": [
        {
            "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', ''))  $(defHandler('-ActProbThresh', WDLCommandPart('NonNull(inputs.activeProbabilityThreshold)', '0.002')))  $(defHandler('-activeRegionExtension', WDLCommandPart('NonNull(inputs.activeRegionExtension)', ' ')))  $(defHandler('-AR', WDLCommandPart('NonNull(inputs.activeRegionIn)', ' ')))  $(defHandler('-activeRegionMaxSize', WDLCommandPart('NonNull(inputs.activeRegionMaxSize)', ' ')))  $(defHandler('-ARO', WDLCommandPart('NonNull(inputs.activeRegionOut)', ' ')))  $(defHandler('-APO', WDLCommandPart('NonNull(inputs.activityProfileOut)', ' ')))  $(defHandler('-alleles', WDLCommandPart('NonNull(inputs.alleles)', 'none')))  $(defHandler('-allowNonUniqueKmersInRef', WDLCommandPart('NonNull(inputs.allowNonUniqueKmersInRef)', 'false')))  $(defHandler('-allSitePLs', WDLCommandPart('NonNull(inputs.allSitePLs)', 'false')))  $(defHandler('-nda', WDLCommandPart('NonNull(inputs.annotateNDA)', 'false')))  $(defHandler('-A', WDLCommandPart('NonNull(inputs.annotation)', '[]')))  $(defHandler('-bamout', WDLCommandPart('NonNull(inputs.bamOutput)', ' ')))  $(defHandler('-bamWriterType', WDLCommandPart('NonNull(inputs.bamWriterType)', 'CALLED_HAPLOTYPES')))  $(defHandler('-bandPassSigma', WDLCommandPart('NonNull(inputs.bandPassSigma)', ' ')))  $(defHandler('-comp', WDLCommandPart('NonNull(inputs.comp)', '[]')))  $(defHandler('-consensus', WDLCommandPart('NonNull(inputs.consensus)', 'false')))  $(defHandler('-contaminationFile', WDLCommandPart('NonNull(inputs.contamination_fraction_per_sample_file)', ' ')))  $(defHandler('-contamination', WDLCommandPart('NonNull(inputs.contamination_fraction_to_filter)', '0.0')))  $(defHandler('-D', WDLCommandPart('NonNull(inputs.dbsnp)', 'none')))  $(defHandler('-debug', WDLCommandPart('NonNull(inputs.debug)', 'false')))  $(defHandler('-disableOptimizations', WDLCommandPart('NonNull(inputs.disableOptimizations)', 'false')))  $(defHandler('-doNotRunPhysicalPhasing', WDLCommandPart('NonNull(inputs.doNotRunPhysicalPhasing)', 'false')))  $(defHandler('-dontIncreaseKmerSizesForCycles', WDLCommandPart('NonNull(inputs.dontIncreaseKmerSizesForCycles)', 'false')))  $(defHandler('-dontTrimActiveRegions', WDLCommandPart('NonNull(inputs.dontTrimActiveRegions)', 'false')))  $(defHandler('-dontUseSoftClippedBases', WDLCommandPart('NonNull(inputs.dontUseSoftClippedBases)', 'false')))  $(defHandler('-edr', WDLCommandPart('NonNull(inputs.emitDroppedReads)', 'false')))  $(defHandler('-ERC', WDLCommandPart('NonNull(inputs.emitRefConfidence)', 'false')))  $(defHandler('-XA', WDLCommandPart('NonNull(inputs.excludeAnnotation)', '[]')))  $(defHandler('-forceActive', WDLCommandPart('NonNull(inputs.forceActive)', 'false')))  $(defHandler('-gcpHMM', WDLCommandPart('NonNull(inputs.gcpHMM)', '10')))  $(defHandler('-gt_mode', WDLCommandPart('NonNull(inputs.genotyping_mode)', 'DISCOVERY')))  $(defHandler('-graph', WDLCommandPart('NonNull(inputs.graphOutput)', ' ')))  $(defHandler('-G', WDLCommandPart('NonNull(inputs.group)', '[StandardAnnotation, StandardHCAnnotation]')))  $(defHandler('-GQB', WDLCommandPart('NonNull(inputs.GVCFGQBands)', '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 70, 80, 90, 99]')))  $(defHandler('-hets', WDLCommandPart('NonNull(inputs.heterozygosity)', '0.001')))  $(defHandler('-heterozygosityStandardDeviation', WDLCommandPart('NonNull(inputs.heterozygosity_stdev)', '0.01')))  $(defHandler('-indelHeterozygosity', WDLCommandPart('NonNull(inputs.indel_heterozygosity)', '1.25E-4')))  $(defHandler('-ERCIS', WDLCommandPart('NonNull(inputs.indelSizeToEliminateInRefModel)', '10')))  $(defHandler('-inputPrior', WDLCommandPart('NonNull(inputs.input_prior)', '[]')))  $(defHandler('-kmerSize', WDLCommandPart('NonNull(inputs.kmerSize)', '[10, 25]')))  $(defHandler('-maxAltAlleles', WDLCommandPart('NonNull(inputs.max_alternate_alleles)', '6')))  $(defHandler('-maxGT', WDLCommandPart('NonNull(inputs.max_genotype_count)', '1024')))  $(defHandler('-maxNumPLValues', WDLCommandPart('NonNull(inputs.max_num_PL_values)', '100')))  $(defHandler('-maxNumHaplotypesInPopulation', WDLCommandPart('NonNull(inputs.maxNumHaplotypesInPopulation)', '128')))  $(defHandler('-maxReadsInMemoryPerSample', WDLCommandPart('NonNull(inputs.maxReadsInMemoryPerSample)', '30000')))  $(defHandler('-maxReadsInRegionPerSample', WDLCommandPart('NonNull(inputs.maxReadsInRegionPerSample)', '10000')))  $(defHandler('-maxTotalReadsInMemory', WDLCommandPart('NonNull(inputs.maxTotalReadsInMemory)', '10000000')))  $(defHandler('-mbq', WDLCommandPart('NonNull(inputs.min_base_quality_score)', '10')))  $(defHandler('-minDanglingBranchLength', WDLCommandPart('NonNull(inputs.minDanglingBranchLength)', '4')))  $(defHandler('-minPruning', WDLCommandPart('NonNull(inputs.minPruning)', '2')))  $(defHandler('-minReadsPerAlignStart', WDLCommandPart('NonNull(inputs.minReadsPerAlignmentStart)', '10')))  $(defHandler('-numPruningSamples', WDLCommandPart('NonNull(inputs.numPruningSamples)', '1')))  $(defHandler('-o', WDLCommandPart('NonNull(inputs.out)', 'stdout')))  $(defHandler('-out_mode', WDLCommandPart('NonNull(inputs.output_mode)', 'EMIT_VARIANTS_ONLY')))  $(defHandler('-pcrModel', WDLCommandPart('NonNull(inputs.pcr_indel_model)', 'CONSERVATIVE')))  $(defHandler('-globalMAPQ', WDLCommandPart('NonNull(inputs.phredScaledGlobalReadMismappingRate)', '45')))  $(defHandler('-sn', WDLCommandPart('NonNull(inputs.sample_name)', ' ')))  $(defHandler('-ploidy', WDLCommandPart('NonNull(inputs.sample_ploidy)', '2')))  $(defHandler('-stand_call_conf', WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_calling)', '10.0')))  $(defHandler('-allelesTrigger', WDLCommandPart('NonNull(inputs.useAllelesTrigger)', 'false')))  $(defHandler('-useFilteredReadsForAnnotations', WDLCommandPart('NonNull(inputs.useFilteredReadsForAnnotations)', 'false')))  $(defHandler('-newQual', WDLCommandPart('NonNull(inputs.useNewAFCalculator)', 'false')))",
            "shellQuote": false
        }
    ],
    "baseCommand": []
}