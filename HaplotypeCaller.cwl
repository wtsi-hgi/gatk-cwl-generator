{
    "id": "HaplotypeCaller",
    "cwlVersion": "v1.0",
    "inputs": [
        {
            "doc": "fasta file of reference genome",
            "type": "File",
            "id": "ref",
            "secondaryFiles": [
                ".fai",
                "^.dict"
            ]
        },
        {
            "doc": "Index file of reference genome",
            "type": "File",
            "id": "refIndex"
        },
        {
            "doc": "dict file of reference genome",
            "type": "File",
            "id": "refDict"
        },
        {
            "doc": "Input file containing sequence data (BAM or CRAM)",
            "type": "File",
            "id": "input_file",
            "secondaryFiles": [
                ".crai"
            ]
        },
        {
            "doc": "Threshold for the probability of a profile state being active.",
            "id": "activeProbabilityThreshold",
            "type": "float?"
        },
        {
            "doc": "The active region extension; if not provided defaults to Walker annotated default",
            "id": "activeRegionExtension",
            "type": "int?"
        },
        {
            "doc": "Use this interval list file as the active regions to process",
            "id": "activeRegionIn",
            "type": "string[]?"
        },
        {
            "doc": "The active region maximum size; if not provided defaults to Walker annotated default",
            "id": "activeRegionMaxSize",
            "type": "int?"
        },
        {
            "doc": "Output the active region to this IGV formatted file",
            "id": "activeRegionOut",
            "type": "string?"
        },
        {
            "doc": "Output the raw activity profile results in IGV format",
            "id": "activityProfileOut",
            "type": "string?"
        },
        {
            "doc": "Set of alleles to use in genotyping",
            "id": "alleles",
            "type": "string?"
        },
        {
            "doc": "Allow graphs that have non-unique kmers in the reference",
            "id": "allowNonUniqueKmersInRef",
            "type": "boolean?"
        },
        {
            "doc": "Annotate all sites with PLs",
            "id": "allSitePLs",
            "type": "boolean?"
        },
        {
            "doc": "Annotate number of alleles observed",
            "id": "annotateNDA",
            "type": "boolean?"
        },
        {
            "doc": "One or more specific annotations to apply to variant calls",
            "id": "annotation",
            "type": "string[]?"
        },
        {
            "doc": "File to which assembled haplotypes should be written",
            "id": "bamOutput",
            "type": "string?"
        },
        {
            "doc": "Which haplotypes should be written to the BAM",
            "id": "bamWriterType",
            "type": "string?"
        },
        {
            "doc": "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default",
            "id": "bandPassSigma",
            "type": "float?"
        },
        {
            "doc": "Comparison VCF file",
            "id": "comp",
            "type": "string[]?"
        },
        {
            "doc": "1000G consensus mode",
            "id": "consensus",
            "type": "boolean?"
        },
        {
            "doc": "Contamination per sample",
            "id": "contamination_fraction_per_sample_file",
            "type": "File?"
        },
        {
            "doc": "Fraction of contamination to aggressively remove",
            "id": "contamination_fraction_to_filter",
            "type": "float?"
        },
        {
            "doc": "dbSNP file",
            "id": "dbsnp",
            "type": "string?"
        },
        {
            "doc": "Print out very verbose debug information about each triggering active region",
            "id": "debug",
            "type": "boolean?"
        },
        {
            "doc": "Don't skip calculations in ActiveRegions with no variants",
            "id": "disableOptimizations",
            "type": "boolean?"
        },
        {
            "doc": "Disable physical phasing",
            "id": "doNotRunPhysicalPhasing",
            "type": "boolean?"
        },
        {
            "doc": "Disable iterating over kmer sizes when graph cycles are detected",
            "id": "dontIncreaseKmerSizesForCycles",
            "type": "boolean?"
        },
        {
            "doc": "If specified, we will not trim down the active region from the full region (active + extension) to just the active interval for genotyping",
            "id": "dontTrimActiveRegions",
            "type": "boolean?"
        },
        {
            "doc": "Do not analyze soft clipped bases in the reads",
            "id": "dontUseSoftClippedBases",
            "type": "boolean?"
        },
        {
            "doc": "Emit reads that are dropped for filtering, trimming, realignment failure",
            "id": "emitDroppedReads",
            "type": "boolean?"
        },
        {
            "doc": "Mode for emitting reference confidence scores",
            "id": "emitRefConfidence",
            "type": "string?"
        },
        {
            "doc": "One or more specific annotations to exclude",
            "id": "excludeAnnotation",
            "type": "string[]?"
        },
        {
            "doc": "If provided, all bases will be tagged as active",
            "id": "forceActive",
            "type": "boolean?"
        },
        {
            "doc": "Flat gap continuation penalty for use in the Pair HMM",
            "id": "gcpHMM",
            "type": "string?"
        },
        {
            "doc": "Specifies how to determine the alternate alleles to use for genotyping",
            "id": "genotyping_mode",
            "type": "string?"
        },
        {
            "doc": "Write debug assembly graph information to this file",
            "id": "graphOutput",
            "type": "string?"
        },
        {
            "doc": "One or more classes/groups of annotations to apply to variant calls",
            "id": "group",
            "type": "string[]?"
        },
        {
            "doc": "Exclusive upper bounds for reference confidence GQ bands (must be in [1, 100] and specified in increasing order)",
            "id": "GVCFGQBands",
            "type": "int[]?"
        },
        {
            "doc": "Heterozygosity value used to compute prior likelihoods for any locus",
            "id": "heterozygosity",
            "type": "float?"
        },
        {
            "doc": "Standard deviation of eterozygosity for SNP and indel calling.",
            "id": "heterozygosity_stdev",
            "type": "float?"
        },
        {
            "doc": "Heterozygosity for indel calling",
            "id": "indel_heterozygosity",
            "type": "float?"
        },
        {
            "doc": "The size of an indel to check for in the reference model",
            "id": "indelSizeToEliminateInRefModel",
            "type": "string?"
        },
        {
            "doc": "Input prior for calls",
            "id": "input_prior",
            "type": "float[]?"
        },
        {
            "doc": "Kmer size to use in the read threading assembler",
            "id": "kmerSize",
            "type": "int[]?"
        },
        {
            "doc": "Maximum number of alternate alleles to genotype",
            "id": "max_alternate_alleles",
            "type": "string?"
        },
        {
            "doc": "Maximum number of genotypes to consider at any site",
            "id": "max_genotype_count",
            "type": "string?"
        },
        {
            "doc": "Maximum number of PL values to output",
            "id": "max_num_PL_values",
            "type": "string?"
        },
        {
            "doc": "Maximum number of haplotypes to consider for your population",
            "id": "maxNumHaplotypesInPopulation",
            "type": "string?"
        },
        {
            "doc": "Maximum reads per sample given to traversal map() function",
            "id": "maxReadsInMemoryPerSample",
            "type": "string?"
        },
        {
            "doc": "Maximum reads in an active region",
            "id": "maxReadsInRegionPerSample",
            "type": "string?"
        },
        {
            "doc": "Maximum total reads given to traversal map() function",
            "id": "maxTotalReadsInMemory",
            "type": "string?"
        },
        {
            "doc": "Minimum base quality required to consider a base for calling",
            "id": "min_base_quality_score",
            "type": "string?"
        },
        {
            "doc": "Minimum length of a dangling branch to attempt recovery",
            "id": "minDanglingBranchLength",
            "type": "string?"
        },
        {
            "doc": "Minimum support to not prune paths in the graph",
            "id": "minPruning",
            "type": "string?"
        },
        {
            "doc": "Minimum number of reads sharing the same alignment start for each genomic location in an active region",
            "id": "minReadsPerAlignmentStart",
            "type": "string?"
        },
        {
            "doc": "Number of samples that must pass the minPruning threshold",
            "id": "numPruningSamples",
            "type": "string?"
        },
        {
            "doc": "File to which variants should be written",
            "id": "out",
            "type": "string?"
        },
        {
            "doc": "Which type of calls we should output",
            "id": "output_mode",
            "type": "string?"
        },
        {
            "doc": "The PCR indel model to use",
            "id": "pcr_indel_model",
            "type": "string?"
        },
        {
            "doc": "The global assumed mismapping rate for reads",
            "id": "phredScaledGlobalReadMismappingRate",
            "type": "string?"
        },
        {
            "doc": "Name of single sample to use from a multi-sample bam",
            "id": "sample_name",
            "type": "string?"
        },
        {
            "doc": "Ploidy per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy).",
            "id": "sample_ploidy",
            "type": "string?"
        },
        {
            "doc": "The minimum phred-scaled confidence threshold at which variants should be called",
            "id": "standard_min_confidence_threshold_for_calling",
            "type": "float?"
        },
        {
            "doc": "Use additional trigger on variants found in an external alleles file",
            "id": "useAllelesTrigger",
            "type": "boolean?"
        },
        {
            "doc": "Use the contamination-filtered read maps for the purposes of annotating variants",
            "id": "useFilteredReadsForAnnotations",
            "type": "boolean?"
        },
        {
            "doc": "Use new AF model instead of the so-called exact model",
            "id": "useNewAFCalculator",
            "type": "boolean?"
        },
        {
            "doc": "Ignore warnings about base quality score encoding",
            "id": "allow_potentially_misencoded_quality_scores",
            "type": "boolean?"
        },
        {
            "doc": "Name of the tool to run",
            "id": "analysis_type",
            "type": "string"
        },
        {
            "doc": "Compression level to use for writing BAM files (0 - 9, higher is more compressed)",
            "id": "bam_compression",
            "type": "int?"
        },
        {
            "doc": "Type of BAQ calculation to apply in the engine",
            "id": "baq",
            "type": "string?"
        },
        {
            "doc": "BAQ gap open penalty",
            "id": "baqGapOpenPenalty",
            "type": "float?"
        },
        {
            "doc": "Input covariates table file for on-the-fly base quality score recalibration",
            "id": "BQSR",
            "type": "File?"
        },
        {
            "doc": "Assign a default base quality",
            "id": "defaultBaseQualities",
            "type": "string?"
        },
        {
            "doc": "Disable both auto-generation of index files and index file locking",
            "id": "disable_auto_index_creation_and_locking_when_reading_rods",
            "type": "boolean?"
        },
        {
            "doc": "Turn off on-the-fly creation of indices for output BAM/CRAM files",
            "id": "disable_bam_indexing",
            "type": "boolean?"
        },
        {
            "doc": "Disable printing of base insertion and deletion tags (with -BQSR)",
            "id": "disable_indel_quals",
            "type": "boolean?"
        },
        {
            "doc": "Read filters to disable",
            "id": "disable_read_filter",
            "type": "string[]?"
        },
        {
            "doc": "Target coverage threshold for downsampling to coverage",
            "id": "downsample_to_coverage",
            "type": "int?"
        },
        {
            "doc": "Fraction of reads to downsample to",
            "id": "downsample_to_fraction",
            "type": "float?"
        },
        {
            "doc": "Type of read downsampling to employ at a given locus",
            "id": "downsampling_type",
            "type": "string?"
        },
        {
            "doc": "Emit the OQ tag with the original base qualities (with -BQSR)",
            "id": "emit_original_quals",
            "type": "boolean?"
        },
        {
            "doc": "One or more genomic intervals to exclude from processing",
            "id": "excludeIntervals",
            "type": "string[]?"
        },
        {
            "doc": "Fix mis-encoded base quality scores",
            "id": "fix_misencoded_quality_scores",
            "type": "boolean?"
        },
        {
            "doc": "Enable on-the-fly creation of md5s for output BAM files.",
            "id": "generate_md5",
            "type": "boolean?"
        },
        {
            "doc": "Global Qscore Bayesian prior to use for BQSR",
            "id": "globalQScorePrior",
            "type": "float?"
        },
        {
            "doc": "Generate the help message",
            "id": "help",
            "type": "boolean?"
        },
        {
            "doc": "Interval merging rule for abutting intervals",
            "id": "interval_merging",
            "type": "string?"
        },
        {
            "doc": "Amount of padding (in bp) to add to each interval",
            "id": "interval_padding",
            "type": "string?"
        },
        {
            "doc": "Set merging approach to use for combining interval inputs",
            "id": "interval_set_rule",
            "type": "string?"
        },
        {
            "doc": "One or more genomic intervals over which to operate",
            "id": "intervals",
            "type": "string[]?"
        },
        {
            "doc": "Keep program records in the SAM header",
            "id": "keep_program_records",
            "type": "boolean?"
        },
        {
            "doc": "Set the logging location",
            "id": "log_to_file",
            "type": "string?"
        },
        {
            "doc": "Set the minimum level of logging",
            "id": "logging_level",
            "type": "string?"
        },
        {
            "doc": "Stop execution cleanly as soon as maxRuntime has been reached",
            "id": "maxRuntime",
            "type": "string?"
        },
        {
            "doc": "Unit of time used by maxRuntime",
            "id": "maxRuntimeUnits",
            "type": "string?"
        },
        {
            "doc": "Enable threading efficiency monitoring",
            "id": "monitorThreadEfficiency",
            "type": "boolean?"
        },
        {
            "doc": "Always output all the records in VCF FORMAT fields, even if some are missing",
            "id": "never_trim_vcf_format_field",
            "type": "boolean?"
        },
        {
            "doc": "Don't include the command line in output VCF headers",
            "id": "no_cmdline_in_header",
            "type": "boolean?"
        },
        {
            "doc": "Use a non-deterministic random seed",
            "id": "nonDeterministicRandomSeed",
            "type": "boolean?"
        },
        {
            "doc": "Number of CPU threads to allocate per data thread",
            "id": "num_cpu_threads_per_data_thread",
            "type": "string?"
        },
        {
            "doc": "Number of data threads to allocate to this analysis",
            "id": "num_threads",
            "type": "int?"
        },
        {
            "doc": "Pedigree files for samples",
            "id": "pedigree",
            "type": "File[]?"
        },
        {
            "doc": "Pedigree string for samples",
            "id": "pedigreeString",
            "type": "string[]?"
        },
        {
            "doc": "Validation strictness for pedigree",
            "id": "pedigreeValidationType",
            "type": "string?"
        },
        {
            "doc": "Write GATK runtime performance log to this file",
            "id": "performanceLog",
            "type": "File?"
        },
        {
            "doc": "Don't recalibrate bases with quality scores less than this threshold (with -BQSR)",
            "id": "preserve_qscores_less_than",
            "type": "string?"
        },
        {
            "doc": "Quantize quality scores to a given number of levels (with -BQSR)",
            "id": "quantize_quals",
            "type": "string?"
        },
        {
            "doc": "Number of reads per SAM file to buffer in memory",
            "id": "read_buffer_size",
            "type": "int?"
        },
        {
            "doc": "Filters to apply to reads before analysis",
            "id": "read_filter",
            "type": "string[]?"
        },
        {
            "doc": "Exclude read groups based on tags",
            "id": "read_group_black_list",
            "type": "string[]?"
        },
        {
            "doc": "Reduce NDN elements in CIGAR string",
            "id": "refactor_NDN_cigar_string",
            "type": "boolean?"
        },
        {
            "doc": "Reference sequence file",
            "id": "reference_sequence",
            "type": "File?"
        },
        {
            "doc": "Reference window stop",
            "id": "reference_window_stop",
            "type": "string?"
        },
        {
            "doc": "Remove program records from the SAM header",
            "id": "remove_program_records",
            "type": "boolean?"
        },
        {
            "doc": "Rename sample IDs on-the-fly at runtime using the provided mapping file",
            "id": "sample_rename_mapping_file",
            "type": "File?"
        },
        {
            "doc": "Time interval for process meter information output (in seconds)",
            "id": "secondsBetweenProgressUpdates",
            "type": "string?"
        },
        {
            "doc": "Emit list of input BAM/CRAM files to log",
            "id": "showFullBamList",
            "type": "boolean?"
        },
        {
            "doc": "Strip down read content and tags",
            "id": "simplifyBAM",
            "type": "boolean?"
        },
        {
            "doc": "Output sites-only VCF",
            "id": "sites_only",
            "type": "boolean?"
        },
        {
            "doc": "Use static quantized quality scores to a given number of levels (with -BQSR)",
            "id": "static_quantized_quals",
            "type": "int[]?"
        },
        {
            "doc": "Enable unsafe operations: nothing will be checked at runtime",
            "id": "unsafe",
            "type": "string?"
        },
        {
            "doc": "Use the base quality scores from the OQ tag",
            "id": "useOriginalQualities",
            "type": "boolean?"
        },
        {
            "doc": "How strict should we be with validation",
            "id": "validation_strictness",
            "type": "string?"
        },
        {
            "doc": "Parameter to pass to the VCF/BCF IndexCreator",
            "id": "variant_index_parameter",
            "type": "string?"
        },
        {
            "doc": "Type of IndexCreator to use for VCF/BCF indices",
            "id": "variant_index_type",
            "type": "string?"
        },
        {
            "doc": "Output version information",
            "id": "version",
            "type": "boolean?"
        }
    ],
    "requirements": [
        {
            "class": "ShellCommandRequirement"
        },
        {
            "class": "InlineJavascriptRequirement",
            "expressionLib": [
                "function WDLCommandPart(expr, def) {var rval; try {rval = eval(expr);} catch(err) {rval = def;} return rval;}",
                "function NonNull(x) {if(x === null) {throw new UserException('NullValue');} else {return x;}}",
                "function defHandler(com, def) {if(Array.isArray(def) && def.length == 0) {return '';} else if(Array.isArray(def) && def.length !=0 ) {return def.map(elementh=> com+ ' ' + element).join(' ');} else if (def =='false') {return '';} else if (def == 'true') {return com;} if (def == []) {return '';} else {return com + def;}}"
            ]
        },
        {
            "dockerPull": "gatk:latest",
            "class": "DockerRequirement"
        }
    ],
    "baseCommand": [],
    "class": "CommandLineTool",
    "arguments": [
        {
            "shellQuote": false,
            "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', ''))  $(defHandler('-ActProbThresh', WDLCommandPart('NonNull(inputs.activeProbabilityThreshold)', '0.002')))  $(defHandler('-activeRegionExtension', WDLCommandPart('NonNull(inputs.activeRegionExtension)', ' ')))  $(defHandler('-AR', WDLCommandPart('NonNull(inputs.activeRegionIn)', ' ')))  $(defHandler('-activeRegionMaxSize', WDLCommandPart('NonNull(inputs.activeRegionMaxSize)', ' ')))  $(defHandler('-ARO', WDLCommandPart('NonNull(inputs.activeRegionOut)', ' ')))  $(defHandler('-APO', WDLCommandPart('NonNull(inputs.activityProfileOut)', ' ')))  $(defHandler('-alleles', WDLCommandPart('NonNull(inputs.alleles)', 'none')))  $(defHandler('-allowNonUniqueKmersInRef', WDLCommandPart('NonNull(inputs.allowNonUniqueKmersInRef)', 'false')))  $(defHandler('-allSitePLs', WDLCommandPart('NonNull(inputs.allSitePLs)', 'false')))  $(defHandler('-nda', WDLCommandPart('NonNull(inputs.annotateNDA)', 'false')))  $(defHandler('-A', WDLCommandPart('NonNull(inputs.annotation)', '[]')))  $(defHandler('-bamout', WDLCommandPart('NonNull(inputs.bamOutput)', ' ')))  $(defHandler('-bamWriterType', WDLCommandPart('NonNull(inputs.bamWriterType)', 'CALLED_HAPLOTYPES')))  $(defHandler('-bandPassSigma', WDLCommandPart('NonNull(inputs.bandPassSigma)', ' ')))  $(defHandler('-comp', WDLCommandPart('NonNull(inputs.comp)', '[]')))  $(defHandler('-consensus', WDLCommandPart('NonNull(inputs.consensus)', 'false')))  $(defHandler('-contaminationFile', WDLCommandPart('NonNull(inputs.contamination_fraction_per_sample_file)', ' ')))  $(defHandler('-contamination', WDLCommandPart('NonNull(inputs.contamination_fraction_to_filter)', '0.0')))  $(defHandler('-D', WDLCommandPart('NonNull(inputs.dbsnp)', 'none')))  $(defHandler('-debug', WDLCommandPart('NonNull(inputs.debug)', 'false')))  $(defHandler('-disableOptimizations', WDLCommandPart('NonNull(inputs.disableOptimizations)', 'false')))  $(defHandler('-doNotRunPhysicalPhasing', WDLCommandPart('NonNull(inputs.doNotRunPhysicalPhasing)', 'false')))  $(defHandler('-dontIncreaseKmerSizesForCycles', WDLCommandPart('NonNull(inputs.dontIncreaseKmerSizesForCycles)', 'false')))  $(defHandler('-dontTrimActiveRegions', WDLCommandPart('NonNull(inputs.dontTrimActiveRegions)', 'false')))  $(defHandler('-dontUseSoftClippedBases', WDLCommandPart('NonNull(inputs.dontUseSoftClippedBases)', 'false')))  $(defHandler('-edr', WDLCommandPart('NonNull(inputs.emitDroppedReads)', 'false')))  $(defHandler('-ERC', WDLCommandPart('NonNull(inputs.emitRefConfidence)', 'false')))  $(defHandler('-XA', WDLCommandPart('NonNull(inputs.excludeAnnotation)', '[]')))  $(defHandler('-forceActive', WDLCommandPart('NonNull(inputs.forceActive)', 'false')))  $(defHandler('-gcpHMM', WDLCommandPart('NonNull(inputs.gcpHMM)', '10')))  $(defHandler('-gt_mode', WDLCommandPart('NonNull(inputs.genotyping_mode)', 'DISCOVERY')))  $(defHandler('-graph', WDLCommandPart('NonNull(inputs.graphOutput)', ' ')))  $(defHandler('-G', WDLCommandPart('NonNull(inputs.group)', '[StandardAnnotation, StandardHCAnnotation]')))  $(defHandler('-GQB', WDLCommandPart('NonNull(inputs.GVCFGQBands)', '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 70, 80, 90, 99]')))  $(defHandler('-hets', WDLCommandPart('NonNull(inputs.heterozygosity)', '0.001')))  $(defHandler('-heterozygosityStandardDeviation', WDLCommandPart('NonNull(inputs.heterozygosity_stdev)', '0.01')))  $(defHandler('-indelHeterozygosity', WDLCommandPart('NonNull(inputs.indel_heterozygosity)', '1.25E-4')))  $(defHandler('-ERCIS', WDLCommandPart('NonNull(inputs.indelSizeToEliminateInRefModel)', '10')))  $(defHandler('-inputPrior', WDLCommandPart('NonNull(inputs.input_prior)', '[]')))  $(defHandler('-kmerSize', WDLCommandPart('NonNull(inputs.kmerSize)', '[10, 25]')))  $(defHandler('-maxAltAlleles', WDLCommandPart('NonNull(inputs.max_alternate_alleles)', '6')))  $(defHandler('-maxGT', WDLCommandPart('NonNull(inputs.max_genotype_count)', '1024')))  $(defHandler('-maxNumPLValues', WDLCommandPart('NonNull(inputs.max_num_PL_values)', '100')))  $(defHandler('-maxNumHaplotypesInPopulation', WDLCommandPart('NonNull(inputs.maxNumHaplotypesInPopulation)', '128')))  $(defHandler('-maxReadsInMemoryPerSample', WDLCommandPart('NonNull(inputs.maxReadsInMemoryPerSample)', '30000')))  $(defHandler('-maxReadsInRegionPerSample', WDLCommandPart('NonNull(inputs.maxReadsInRegionPerSample)', '10000')))  $(defHandler('-maxTotalReadsInMemory', WDLCommandPart('NonNull(inputs.maxTotalReadsInMemory)', '10000000')))  $(defHandler('-mbq', WDLCommandPart('NonNull(inputs.min_base_quality_score)', '10')))  $(defHandler('-minDanglingBranchLength', WDLCommandPart('NonNull(inputs.minDanglingBranchLength)', '4')))  $(defHandler('-minPruning', WDLCommandPart('NonNull(inputs.minPruning)', '2')))  $(defHandler('-minReadsPerAlignStart', WDLCommandPart('NonNull(inputs.minReadsPerAlignmentStart)', '10')))  $(defHandler('-numPruningSamples', WDLCommandPart('NonNull(inputs.numPruningSamples)', '1')))  $(defHandler('-o', WDLCommandPart('NonNull(inputs.out)', 'stdout')))  $(defHandler('-out_mode', WDLCommandPart('NonNull(inputs.output_mode)', 'EMIT_VARIANTS_ONLY')))  $(defHandler('-pcrModel', WDLCommandPart('NonNull(inputs.pcr_indel_model)', 'CONSERVATIVE')))  $(defHandler('-globalMAPQ', WDLCommandPart('NonNull(inputs.phredScaledGlobalReadMismappingRate)', '45')))  $(defHandler('-sn', WDLCommandPart('NonNull(inputs.sample_name)', ' ')))  $(defHandler('-ploidy', WDLCommandPart('NonNull(inputs.sample_ploidy)', '2')))  $(defHandler('-stand_call_conf', WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_calling)', '10.0')))  $(defHandler('-allelesTrigger', WDLCommandPart('NonNull(inputs.useAllelesTrigger)', 'false')))  $(defHandler('-useFilteredReadsForAnnotations', WDLCommandPart('NonNull(inputs.useFilteredReadsForAnnotations)', 'false')))  $(defHandler('-newQual', WDLCommandPart('NonNull(inputs.useNewAFCalculator)', 'false')))  $(defHandler('-allowPotentiallyMisencodedQuals', WDLCommandPart('NonNull(inputs.allow_potentially_misencoded_quality_scores)', 'false')))  $(defHandler('-T', WDLCommandPart('NonNull(inputs.analysis_type)', ' ')))  $(defHandler('-compress', WDLCommandPart('NonNull(inputs.bam_compression)', ' ')))  $(defHandler('-baq', WDLCommandPart('NonNull(inputs.baq)', 'OFF')))  $(defHandler('-baqGOP', WDLCommandPart('NonNull(inputs.baqGapOpenPenalty)', '40.0')))  $(defHandler('-BQSR', WDLCommandPart('NonNull(inputs.BQSR)', ' ')))  $(defHandler('-DBQ', WDLCommandPart('NonNull(inputs.defaultBaseQualities)', '-1')))  $(defHandler('-disable_auto_index_creation_and_locking_when_reading_rods', WDLCommandPart('NonNull(inputs.disable_auto_index_creation_and_locking_when_reading_rods)', 'false')))  $(defHandler('NA', WDLCommandPart('NonNull(inputs.disable_bam_indexing)', 'false')))  $(defHandler('-DIQ', WDLCommandPart('NonNull(inputs.disable_indel_quals)', 'false')))  $(defHandler('-drf', WDLCommandPart('NonNull(inputs.disable_read_filter)', '[]')))  $(defHandler('-dcov', WDLCommandPart('NonNull(inputs.downsample_to_coverage)', ' ')))  $(defHandler('-dfrac', WDLCommandPart('NonNull(inputs.downsample_to_fraction)', ' ')))  $(defHandler('-dt', WDLCommandPart('NonNull(inputs.downsampling_type)', ' ')))  $(defHandler('-EOQ', WDLCommandPart('NonNull(inputs.emit_original_quals)', 'false')))  $(defHandler('-XL', WDLCommandPart('NonNull(inputs.excludeIntervals)', ' ')))  $(defHandler('-fixMisencodedQuals', WDLCommandPart('NonNull(inputs.fix_misencoded_quality_scores)', 'false')))  $(defHandler('NA', WDLCommandPart('NonNull(inputs.generate_md5)', 'false')))  $(defHandler('-globalQScorePrior', WDLCommandPart('NonNull(inputs.globalQScorePrior)', '-1.0')))  $(defHandler('-h', WDLCommandPart('NonNull(inputs.help)', 'false')))  $(defHandler('-I', WDLCommandPart('NonNull(inputs.input_file)', '[]')))  $(defHandler('-im', WDLCommandPart('NonNull(inputs.interval_merging)', 'ALL')))  $(defHandler('-ip', WDLCommandPart('NonNull(inputs.interval_padding)', '0')))  $(defHandler('-isr', WDLCommandPart('NonNull(inputs.interval_set_rule)', 'UNION')))  $(defHandler('-L', WDLCommandPart('NonNull(inputs.intervals)', ' ')))  $(defHandler('-kpr', WDLCommandPart('NonNull(inputs.keep_program_records)', 'false')))  $(defHandler('-log', WDLCommandPart('NonNull(inputs.log_to_file)', ' ')))  $(defHandler('-l', WDLCommandPart('NonNull(inputs.logging_level)', 'INFO')))  $(defHandler('-maxRuntime', WDLCommandPart('NonNull(inputs.maxRuntime)', '-1')))  $(defHandler('-maxRuntimeUnits', WDLCommandPart('NonNull(inputs.maxRuntimeUnits)', 'MINUTES')))  $(defHandler('-mte', WDLCommandPart('NonNull(inputs.monitorThreadEfficiency)', 'false')))  $(defHandler('-writeFullFormat', WDLCommandPart('NonNull(inputs.never_trim_vcf_format_field)', 'false')))  $(defHandler('-no_cmdline_in_header', WDLCommandPart('NonNull(inputs.no_cmdline_in_header)', 'false')))  $(defHandler('-ndrs', WDLCommandPart('NonNull(inputs.nonDeterministicRandomSeed)', 'false')))  $(defHandler('-nct', WDLCommandPart('NonNull(inputs.num_cpu_threads_per_data_thread)', '1')))  $(defHandler('-nt', WDLCommandPart('NonNull(inputs.num_threads)', '1')))  $(defHandler('-ped', WDLCommandPart('NonNull(inputs.pedigree)', '[]')))  $(defHandler('-pedString', WDLCommandPart('NonNull(inputs.pedigreeString)', '[]')))  $(defHandler('-pedValidationType', WDLCommandPart('NonNull(inputs.pedigreeValidationType)', 'STRICT')))  $(defHandler('-PF', WDLCommandPart('NonNull(inputs.performanceLog)', ' ')))  $(defHandler('-preserveQ', WDLCommandPart('NonNull(inputs.preserve_qscores_less_than)', '6')))  $(defHandler('-qq', WDLCommandPart('NonNull(inputs.quantize_quals)', '0')))  $(defHandler('-rbs', WDLCommandPart('NonNull(inputs.read_buffer_size)', ' ')))  $(defHandler('-rf', WDLCommandPart('NonNull(inputs.read_filter)', '[]')))  $(defHandler('-rgbl', WDLCommandPart('NonNull(inputs.read_group_black_list)', ' ')))  $(defHandler('-fixNDN', WDLCommandPart('NonNull(inputs.refactor_NDN_cigar_string)', 'false')))  $(defHandler('-R', WDLCommandPart('NonNull(inputs.reference_sequence)', ' ')))  $(defHandler('-ref_win_stop', WDLCommandPart('NonNull(inputs.reference_window_stop)', '0')))  $(defHandler('-rpr', WDLCommandPart('NonNull(inputs.remove_program_records)', 'false')))  $(defHandler('-sample_rename_mapping_file', WDLCommandPart('NonNull(inputs.sample_rename_mapping_file)', ' ')))  $(defHandler('-secondsBetweenProgressUpdates', WDLCommandPart('NonNull(inputs.secondsBetweenProgressUpdates)', '10')))  $(defHandler('NA', WDLCommandPart('NonNull(inputs.showFullBamList)', 'false')))  $(defHandler('-simplifyBAM', WDLCommandPart('NonNull(inputs.simplifyBAM)', 'false')))  $(defHandler('-sites_only', WDLCommandPart('NonNull(inputs.sites_only)', 'false')))  $(defHandler('-SQQ', WDLCommandPart('NonNull(inputs.static_quantized_quals)', ' ')))  $(defHandler('-U', WDLCommandPart('NonNull(inputs.unsafe)', ' ')))  $(defHandler('-OQ', WDLCommandPart('NonNull(inputs.useOriginalQualities)', 'false')))  $(defHandler('-S', WDLCommandPart('NonNull(inputs.validation_strictness)', 'SILENT')))  $(defHandler('-variant_index_parameter', WDLCommandPart('NonNull(inputs.variant_index_parameter)', '-1')))  $(defHandler('-variant_index_type', WDLCommandPart('NonNull(inputs.variant_index_type)', 'DYNAMIC_SEEK')))  $(defHandler('-version', WDLCommandPart('NonNull(inputs.version)', 'false')))"
        }
    ],
    "outputs": [
        {
            "outputBinding": {
                "glob": "$(inputs.out)"
            },
            "type": "File",
            "id": "taskOut"
        }
    ]
}