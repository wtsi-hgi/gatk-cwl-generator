{
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
            "type": "float?", 
            "id": "activeProbabilityThreshold"
        }, 
        {
            "doc": "The active region extension; if not provided defaults to Walker annotated default", 
            "type": "int?", 
            "id": "activeRegionExtension"
        }, 
        {
            "doc": "Use this interval list file as the active regions to process", 
            "type": "string[]?", 
            "id": "activeRegionIn"
        }, 
        {
            "doc": "The active region maximum size; if not provided defaults to Walker annotated default", 
            "type": "int?", 
            "id": "activeRegionMaxSize"
        }, 
        {
            "doc": "Output the active region to this IGV formatted file", 
            "type": "string?", 
            "id": "activeRegionOut"
        }, 
        {
            "doc": "Output the raw activity profile results in IGV format", 
            "type": "string?", 
            "id": "activityProfileOut"
        }, 
        {
            "doc": "Set of alleles to use in genotyping", 
            "type": "string?", 
            "id": "alleles"
        }, 
        {
            "doc": "Allow graphs that have non-unique kmers in the reference", 
            "type": "boolean?", 
            "id": "allowNonUniqueKmersInRef"
        }, 
        {
            "doc": "Annotate all sites with PLs", 
            "type": "boolean?", 
            "id": "allSitePLs"
        }, 
        {
            "doc": "Annotate number of alleles observed", 
            "type": "boolean?", 
            "id": "annotateNDA"
        }, 
        {
            "doc": "One or more specific annotations to apply to variant calls", 
            "type": "string[]?", 
            "id": "annotation"
        }, 
        {
            "doc": "File to which assembled haplotypes should be written", 
            "type": "string?", 
            "id": "bamOutput"
        }, 
        {
            "doc": "Which haplotypes should be written to the BAM", 
            "type": "string?", 
            "id": "bamWriterType"
        }, 
        {
            "doc": "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default", 
            "type": "float?", 
            "id": "bandPassSigma"
        }, 
        {
            "doc": "Comparison VCF file", 
            "type": "string[]?", 
            "id": "comp"
        }, 
        {
            "doc": "1000G consensus mode", 
            "type": "boolean?", 
            "id": "consensus"
        }, 
        {
            "doc": "Contamination per sample", 
            "type": "File?", 
            "id": "contamination_fraction_per_sample_file"
        }, 
        {
            "doc": "Fraction of contamination to aggressively remove", 
            "type": "float?", 
            "id": "contamination_fraction_to_filter"
        }, 
        {
            "doc": "dbSNP file", 
            "type": "string?", 
            "id": "dbsnp"
        }, 
        {
            "doc": "Print out very verbose debug information about each triggering active region", 
            "type": "boolean?", 
            "id": "debug"
        }, 
        {
            "doc": "Don't skip calculations in ActiveRegions with no variants", 
            "type": "boolean?", 
            "id": "disableOptimizations"
        }, 
        {
            "doc": "Disable physical phasing", 
            "type": "boolean?", 
            "id": "doNotRunPhysicalPhasing"
        }, 
        {
            "doc": "Disable iterating over kmer sizes when graph cycles are detected", 
            "type": "boolean?", 
            "id": "dontIncreaseKmerSizesForCycles"
        }, 
        {
            "doc": "If specified, we will not trim down the active region from the full region (active + extension) to just the active interval for genotyping", 
            "type": "boolean?", 
            "id": "dontTrimActiveRegions"
        }, 
        {
            "doc": "Do not analyze soft clipped bases in the reads", 
            "type": "boolean?", 
            "id": "dontUseSoftClippedBases"
        }, 
        {
            "doc": "Emit reads that are dropped for filtering, trimming, realignment failure", 
            "type": "boolean?", 
            "id": "emitDroppedReads"
        }, 
        {
            "doc": "Mode for emitting reference confidence scores", 
            "type": "string?", 
            "id": "emitRefConfidence"
        }, 
        {
            "doc": "One or more specific annotations to exclude", 
            "type": "string[]?", 
            "id": "excludeAnnotation"
        }, 
        {
            "doc": "If provided, all bases will be tagged as active", 
            "type": "boolean?", 
            "id": "forceActive"
        }, 
        {
            "doc": "Flat gap continuation penalty for use in the Pair HMM", 
            "type": "string?", 
            "id": "gcpHMM"
        }, 
        {
            "doc": "Specifies how to determine the alternate alleles to use for genotyping", 
            "type": "string?", 
            "id": "genotyping_mode"
        }, 
        {
            "doc": "Write debug assembly graph information to this file", 
            "type": "string?", 
            "id": "graphOutput"
        }, 
        {
            "doc": "One or more classes/groups of annotations to apply to variant calls", 
            "type": "string[]?", 
            "id": "group"
        }, 
        {
            "doc": "Exclusive upper bounds for reference confidence GQ bands (must be in [1, 100] and specified in increasing order)", 
            "type": "int[]?", 
            "id": "GVCFGQBands"
        }, 
        {
            "doc": "Heterozygosity value used to compute prior likelihoods for any locus", 
            "type": "float?", 
            "id": "heterozygosity"
        }, 
        {
            "doc": "Standard deviation of eterozygosity for SNP and indel calling.", 
            "type": "float?", 
            "id": "heterozygosity_stdev"
        }, 
        {
            "doc": "Heterozygosity for indel calling", 
            "type": "float?", 
            "id": "indel_heterozygosity"
        }, 
        {
            "doc": "The size of an indel to check for in the reference model", 
            "type": "string?", 
            "id": "indelSizeToEliminateInRefModel"
        }, 
        {
            "doc": "Input prior for calls", 
            "type": "float[]?", 
            "id": "input_prior"
        }, 
        {
            "doc": "Kmer size to use in the read threading assembler", 
            "type": "int[]?", 
            "id": "kmerSize"
        }, 
        {
            "doc": "Maximum number of alternate alleles to genotype", 
            "type": "string?", 
            "id": "max_alternate_alleles"
        }, 
        {
            "doc": "Maximum number of genotypes to consider at any site", 
            "type": "string?", 
            "id": "max_genotype_count"
        }, 
        {
            "doc": "Maximum number of PL values to output", 
            "type": "string?", 
            "id": "max_num_PL_values"
        }, 
        {
            "doc": "Maximum number of haplotypes to consider for your population", 
            "type": "string?", 
            "id": "maxNumHaplotypesInPopulation"
        }, 
        {
            "doc": "Maximum reads per sample given to traversal map() function", 
            "type": "string?", 
            "id": "maxReadsInMemoryPerSample"
        }, 
        {
            "doc": "Maximum reads in an active region", 
            "type": "string?", 
            "id": "maxReadsInRegionPerSample"
        }, 
        {
            "doc": "Maximum total reads given to traversal map() function", 
            "type": "string?", 
            "id": "maxTotalReadsInMemory"
        }, 
        {
            "doc": "Minimum base quality required to consider a base for calling", 
            "type": "string?", 
            "id": "min_base_quality_score"
        }, 
        {
            "doc": "Minimum length of a dangling branch to attempt recovery", 
            "type": "string?", 
            "id": "minDanglingBranchLength"
        }, 
        {
            "doc": "Minimum support to not prune paths in the graph", 
            "type": "string?", 
            "id": "minPruning"
        }, 
        {
            "doc": "Minimum number of reads sharing the same alignment start for each genomic location in an active region", 
            "type": "string?", 
            "id": "minReadsPerAlignmentStart"
        }, 
        {
            "doc": "Number of samples that must pass the minPruning threshold", 
            "type": "string?", 
            "id": "numPruningSamples"
        }, 
        {
            "doc": "File to which variants should be written", 
            "type": "string?", 
            "id": "out"
        }, 
        {
            "doc": "Which type of calls we should output", 
            "type": "string?", 
            "id": "output_mode"
        }, 
        {
            "doc": "The PCR indel model to use", 
            "type": "string?", 
            "id": "pcr_indel_model"
        }, 
        {
            "doc": "The global assumed mismapping rate for reads", 
            "type": "string?", 
            "id": "phredScaledGlobalReadMismappingRate"
        }, 
        {
            "doc": "Name of single sample to use from a multi-sample bam", 
            "type": "string?", 
            "id": "sample_name"
        }, 
        {
            "doc": "Ploidy per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy).", 
            "type": "string?", 
            "id": "sample_ploidy"
        }, 
        {
            "doc": "The minimum phred-scaled confidence threshold at which variants should be called", 
            "type": "float?", 
            "id": "standard_min_confidence_threshold_for_calling"
        }, 
        {
            "doc": "Use additional trigger on variants found in an external alleles file", 
            "type": "boolean?", 
            "id": "useAllelesTrigger"
        }, 
        {
            "doc": "Use the contamination-filtered read maps for the purposes of annotating variants", 
            "type": "boolean?", 
            "id": "useFilteredReadsForAnnotations"
        }, 
        {
            "doc": "Use new AF model instead of the so-called exact model", 
            "type": "boolean?", 
            "id": "useNewAFCalculator"
        }, 
        {
            "doc": "Ignore warnings about base quality score encoding", 
            "type": "boolean?", 
            "id": "allow_potentially_misencoded_quality_scores"
        }, 
        {
            "doc": "Name of the tool to run", 
            "type": "string", 
            "id": "analysis_type"
        }, 
        {
            "doc": "Compression level to use for writing BAM files (0 - 9, higher is more compressed)", 
            "type": "int?", 
            "id": "bam_compression"
        }, 
        {
            "doc": "Type of BAQ calculation to apply in the engine", 
            "type": "string?", 
            "id": "baq"
        }, 
        {
            "doc": "BAQ gap open penalty", 
            "type": "float?", 
            "id": "baqGapOpenPenalty"
        }, 
        {
            "doc": "Input covariates table file for on-the-fly base quality score recalibration", 
            "type": "File?", 
            "id": "BQSR"
        }, 
        {
            "doc": "Assign a default base quality", 
            "type": "string?", 
            "id": "defaultBaseQualities"
        }, 
        {
            "doc": "Disable both auto-generation of index files and index file locking", 
            "type": "boolean?", 
            "id": "disable_auto_index_creation_and_locking_when_reading_rods"
        }, 
        {
            "doc": "Turn off on-the-fly creation of indices for output BAM/CRAM files", 
            "type": "boolean?", 
            "id": "disable_bam_indexing"
        }, 
        {
            "doc": "Disable printing of base insertion and deletion tags (with -BQSR)", 
            "type": "boolean?", 
            "id": "disable_indel_quals"
        }, 
        {
            "doc": "Read filters to disable", 
            "type": "string[]?", 
            "id": "disable_read_filter"
        }, 
        {
            "doc": "Target coverage threshold for downsampling to coverage", 
            "type": "int?", 
            "id": "downsample_to_coverage"
        }, 
        {
            "doc": "Fraction of reads to downsample to", 
            "type": "float?", 
            "id": "downsample_to_fraction"
        }, 
        {
            "doc": "Type of read downsampling to employ at a given locus", 
            "type": "string?", 
            "id": "downsampling_type"
        }, 
        {
            "doc": "Emit the OQ tag with the original base qualities (with -BQSR)", 
            "type": "boolean?", 
            "id": "emit_original_quals"
        }, 
        {
            "doc": "One or more genomic intervals to exclude from processing", 
            "type": "string[]?", 
            "id": "excludeIntervals"
        }, 
        {
            "doc": "Fix mis-encoded base quality scores", 
            "type": "boolean?", 
            "id": "fix_misencoded_quality_scores"
        }, 
        {
            "doc": "Enable on-the-fly creation of md5s for output BAM files.", 
            "type": "boolean?", 
            "id": "generate_md5"
        }, 
        {
            "doc": "Global Qscore Bayesian prior to use for BQSR", 
            "type": "float?", 
            "id": "globalQScorePrior"
        }, 
        {
            "doc": "Generate the help message", 
            "type": "boolean?", 
            "id": "help"
        }, 
        {
            "doc": "Interval merging rule for abutting intervals", 
            "type": "string?", 
            "id": "interval_merging"
        }, 
        {
            "doc": "Amount of padding (in bp) to add to each interval", 
            "type": "string?", 
            "id": "interval_padding"
        }, 
        {
            "doc": "Set merging approach to use for combining interval inputs", 
            "type": "string?", 
            "id": "interval_set_rule"
        }, 
        {
            "doc": "One or more genomic intervals over which to operate", 
            "type": "string[]?", 
            "id": "intervals"
        }, 
        {
            "doc": "Keep program records in the SAM header", 
            "type": "boolean?", 
            "id": "keep_program_records"
        }, 
        {
            "doc": "Set the logging location", 
            "type": "string?", 
            "id": "log_to_file"
        }, 
        {
            "doc": "Set the minimum level of logging", 
            "type": "string?", 
            "id": "logging_level"
        }, 
        {
            "doc": "Stop execution cleanly as soon as maxRuntime has been reached", 
            "type": "string?", 
            "id": "maxRuntime"
        }, 
        {
            "doc": "Unit of time used by maxRuntime", 
            "type": "string?", 
            "id": "maxRuntimeUnits"
        }, 
        {
            "doc": "Enable threading efficiency monitoring", 
            "type": "boolean?", 
            "id": "monitorThreadEfficiency"
        }, 
        {
            "doc": "Always output all the records in VCF FORMAT fields, even if some are missing", 
            "type": "boolean?", 
            "id": "never_trim_vcf_format_field"
        }, 
        {
            "doc": "Don't include the command line in output VCF headers", 
            "type": "boolean?", 
            "id": "no_cmdline_in_header"
        }, 
        {
            "doc": "Use a non-deterministic random seed", 
            "type": "boolean?", 
            "id": "nonDeterministicRandomSeed"
        }, 
        {
            "doc": "Number of CPU threads to allocate per data thread", 
            "type": "string?", 
            "id": "num_cpu_threads_per_data_thread"
        }, 
        {
            "doc": "Number of data threads to allocate to this analysis", 
            "type": "int?", 
            "id": "num_threads"
        }, 
        {
            "doc": "Pedigree files for samples", 
            "type": "File[]?", 
            "id": "pedigree"
        }, 
        {
            "doc": "Pedigree string for samples", 
            "type": "string[]?", 
            "id": "pedigreeString"
        }, 
        {
            "doc": "Validation strictness for pedigree", 
            "type": "string?", 
            "id": "pedigreeValidationType"
        }, 
        {
            "doc": "Write GATK runtime performance log to this file", 
            "type": "File?", 
            "id": "performanceLog"
        }, 
        {
            "doc": "Don't recalibrate bases with quality scores less than this threshold (with -BQSR)", 
            "type": "string?", 
            "id": "preserve_qscores_less_than"
        }, 
        {
            "doc": "Quantize quality scores to a given number of levels (with -BQSR)", 
            "type": "string?", 
            "id": "quantize_quals"
        }, 
        {
            "doc": "Number of reads per SAM file to buffer in memory", 
            "type": "int?", 
            "id": "read_buffer_size"
        }, 
        {
            "doc": "Filters to apply to reads before analysis", 
            "type": "string[]?", 
            "id": "read_filter"
        }, 
        {
            "doc": "Exclude read groups based on tags", 
            "type": "string[]?", 
            "id": "read_group_black_list"
        }, 
        {
            "doc": "Reduce NDN elements in CIGAR string", 
            "type": "boolean?", 
            "id": "refactor_NDN_cigar_string"
        }, 
        {
            "doc": "Reference sequence file", 
            "type": "File?", 
            "id": "reference_sequence"
        }, 
        {
            "doc": "Reference window stop", 
            "type": "string?", 
            "id": "reference_window_stop"
        }, 
        {
            "doc": "Remove program records from the SAM header", 
            "type": "boolean?", 
            "id": "remove_program_records"
        }, 
        {
            "doc": "Rename sample IDs on-the-fly at runtime using the provided mapping file", 
            "type": "File?", 
            "id": "sample_rename_mapping_file"
        }, 
        {
            "doc": "Time interval for process meter information output (in seconds)", 
            "type": "string?", 
            "id": "secondsBetweenProgressUpdates"
        }, 
        {
            "doc": "Emit list of input BAM/CRAM files to log", 
            "type": "boolean?", 
            "id": "showFullBamList"
        }, 
        {
            "doc": "Strip down read content and tags", 
            "type": "boolean?", 
            "id": "simplifyBAM"
        }, 
        {
            "doc": "Output sites-only VCF", 
            "type": "boolean?", 
            "id": "sites_only"
        }, 
        {
            "doc": "Use static quantized quality scores to a given number of levels (with -BQSR)", 
            "type": "int[]?", 
            "id": "static_quantized_quals"
        }, 
        {
            "doc": "Enable unsafe operations: nothing will be checked at runtime", 
            "type": "string?", 
            "id": "unsafe"
        }, 
        {
            "doc": "Use the base quality scores from the OQ tag", 
            "type": "boolean?", 
            "id": "useOriginalQualities"
        }, 
        {
            "doc": "How strict should we be with validation", 
            "type": "string?", 
            "id": "validation_strictness"
        }, 
        {
            "doc": "Parameter to pass to the VCF/BCF IndexCreator", 
            "type": "string?", 
            "id": "variant_index_parameter"
        }, 
        {
            "doc": "Type of IndexCreator to use for VCF/BCF indices", 
            "type": "string?", 
            "id": "variant_index_type"
        }, 
        {
            "doc": "Output version information", 
            "type": "boolean?", 
            "id": "version"
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
    "outputs": [
        {
            "outputBinding": {
                "glob": "$(inputs.out)"
            }, 
            "type": "File", 
            "id": "taskOut"
        }
    ], 
    "baseCommand": [], 
    "id": "HaplotypeCaller", 
    "arguments": [
        {
            "shellQuote": false, 
            "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', ''))  $(defHandler('-ActProbThresh', WDLCommandPart('NonNull(inputs.activeProbabilityThreshold)', '0.002')))  $(defHandler('-activeRegionExtension', WDLCommandPart('NonNull(inputs.activeRegionExtension)', ' ')))  $(defHandler('-AR', WDLCommandPart('NonNull(inputs.activeRegionIn)', ' ')))  $(defHandler('-activeRegionMaxSize', WDLCommandPart('NonNull(inputs.activeRegionMaxSize)', ' ')))  $(defHandler('-ARO', WDLCommandPart('NonNull(inputs.activeRegionOut)', ' ')))  $(defHandler('-APO', WDLCommandPart('NonNull(inputs.activityProfileOut)', ' ')))  $(defHandler('-alleles', WDLCommandPart('NonNull(inputs.alleles)', 'none')))  $(defHandler('-allowNonUniqueKmersInRef', WDLCommandPart('NonNull(inputs.allowNonUniqueKmersInRef)', 'false')))  $(defHandler('-allSitePLs', WDLCommandPart('NonNull(inputs.allSitePLs)', 'false')))  $(defHandler('-nda', WDLCommandPart('NonNull(inputs.annotateNDA)', 'false')))  $(defHandler('-A', WDLCommandPart('NonNull(inputs.annotation)', '[]')))  $(defHandler('-bamout', WDLCommandPart('NonNull(inputs.bamOutput)', ' ')))  $(defHandler('-bamWriterType', WDLCommandPart('NonNull(inputs.bamWriterType)', 'CALLED_HAPLOTYPES')))  $(defHandler('-bandPassSigma', WDLCommandPart('NonNull(inputs.bandPassSigma)', ' ')))  $(defHandler('-comp', WDLCommandPart('NonNull(inputs.comp)', '[]')))  $(defHandler('-consensus', WDLCommandPart('NonNull(inputs.consensus)', 'false')))  $(defHandler('-contaminationFile', WDLCommandPart('NonNull(inputs.contamination_fraction_per_sample_file)', ' ')))  $(defHandler('-contamination', WDLCommandPart('NonNull(inputs.contamination_fraction_to_filter)', '0.0')))  $(defHandler('-D', WDLCommandPart('NonNull(inputs.dbsnp)', 'none')))  $(defHandler('-debug', WDLCommandPart('NonNull(inputs.debug)', 'false')))  $(defHandler('-disableOptimizations', WDLCommandPart('NonNull(inputs.disableOptimizations)', 'false')))  $(defHandler('-doNotRunPhysicalPhasing', WDLCommandPart('NonNull(inputs.doNotRunPhysicalPhasing)', 'false')))  $(defHandler('-dontIncreaseKmerSizesForCycles', WDLCommandPart('NonNull(inputs.dontIncreaseKmerSizesForCycles)', 'false')))  $(defHandler('-dontTrimActiveRegions', WDLCommandPart('NonNull(inputs.dontTrimActiveRegions)', 'false')))  $(defHandler('-dontUseSoftClippedBases', WDLCommandPart('NonNull(inputs.dontUseSoftClippedBases)', 'false')))  $(defHandler('-edr', WDLCommandPart('NonNull(inputs.emitDroppedReads)', 'false')))  $(defHandler('-ERC', WDLCommandPart('NonNull(inputs.emitRefConfidence)', 'false')))  $(defHandler('-XA', WDLCommandPart('NonNull(inputs.excludeAnnotation)', '[]')))  $(defHandler('-forceActive', WDLCommandPart('NonNull(inputs.forceActive)', 'false')))  $(defHandler('-gcpHMM', WDLCommandPart('NonNull(inputs.gcpHMM)', '10')))  $(defHandler('-gt_mode', WDLCommandPart('NonNull(inputs.genotyping_mode)', 'DISCOVERY')))  $(defHandler('-graph', WDLCommandPart('NonNull(inputs.graphOutput)', ' ')))  $(defHandler('-G', WDLCommandPart('NonNull(inputs.group)', '[StandardAnnotation, StandardHCAnnotation]')))  $(defHandler('-GQB', WDLCommandPart('NonNull(inputs.GVCFGQBands)', '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 70, 80, 90, 99]')))  $(defHandler('-hets', WDLCommandPart('NonNull(inputs.heterozygosity)', '0.001')))  $(defHandler('-heterozygosityStandardDeviation', WDLCommandPart('NonNull(inputs.heterozygosity_stdev)', '0.01')))  $(defHandler('-indelHeterozygosity', WDLCommandPart('NonNull(inputs.indel_heterozygosity)', '1.25E-4')))  $(defHandler('-ERCIS', WDLCommandPart('NonNull(inputs.indelSizeToEliminateInRefModel)', '10')))  $(defHandler('-inputPrior', WDLCommandPart('NonNull(inputs.input_prior)', '[]')))  $(defHandler('-kmerSize', WDLCommandPart('NonNull(inputs.kmerSize)', '[10, 25]')))  $(defHandler('-maxAltAlleles', WDLCommandPart('NonNull(inputs.max_alternate_alleles)', '6')))  $(defHandler('-maxGT', WDLCommandPart('NonNull(inputs.max_genotype_count)', '1024')))  $(defHandler('-maxNumPLValues', WDLCommandPart('NonNull(inputs.max_num_PL_values)', '100')))  $(defHandler('-maxNumHaplotypesInPopulation', WDLCommandPart('NonNull(inputs.maxNumHaplotypesInPopulation)', '128')))  $(defHandler('-maxReadsInMemoryPerSample', WDLCommandPart('NonNull(inputs.maxReadsInMemoryPerSample)', '30000')))  $(defHandler('-maxReadsInRegionPerSample', WDLCommandPart('NonNull(inputs.maxReadsInRegionPerSample)', '10000')))  $(defHandler('-maxTotalReadsInMemory', WDLCommandPart('NonNull(inputs.maxTotalReadsInMemory)', '10000000')))  $(defHandler('-mbq', WDLCommandPart('NonNull(inputs.min_base_quality_score)', '10')))  $(defHandler('-minDanglingBranchLength', WDLCommandPart('NonNull(inputs.minDanglingBranchLength)', '4')))  $(defHandler('-minPruning', WDLCommandPart('NonNull(inputs.minPruning)', '2')))  $(defHandler('-minReadsPerAlignStart', WDLCommandPart('NonNull(inputs.minReadsPerAlignmentStart)', '10')))  $(defHandler('-numPruningSamples', WDLCommandPart('NonNull(inputs.numPruningSamples)', '1')))  $(defHandler('-o', WDLCommandPart('NonNull(inputs.out)', 'stdout')))  $(defHandler('-out_mode', WDLCommandPart('NonNull(inputs.output_mode)', 'EMIT_VARIANTS_ONLY')))  $(defHandler('-pcrModel', WDLCommandPart('NonNull(inputs.pcr_indel_model)', 'CONSERVATIVE')))  $(defHandler('-globalMAPQ', WDLCommandPart('NonNull(inputs.phredScaledGlobalReadMismappingRate)', '45')))  $(defHandler('-sn', WDLCommandPart('NonNull(inputs.sample_name)', ' ')))  $(defHandler('-ploidy', WDLCommandPart('NonNull(inputs.sample_ploidy)', '2')))  $(defHandler('-stand_call_conf', WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_calling)', '10.0')))  $(defHandler('-allelesTrigger', WDLCommandPart('NonNull(inputs.useAllelesTrigger)', 'false')))  $(defHandler('-useFilteredReadsForAnnotations', WDLCommandPart('NonNull(inputs.useFilteredReadsForAnnotations)', 'false')))  $(defHandler('-newQual', WDLCommandPart('NonNull(inputs.useNewAFCalculator)', 'false')))  $(defHandler('-allowPotentiallyMisencodedQuals', WDLCommandPart('NonNull(inputs.allow_potentially_misencoded_quality_scores)', 'false')))  $(defHandler('-T', WDLCommandPart('NonNull(inputs.analysis_type)', ' ')))  $(defHandler('-compress', WDLCommandPart('NonNull(inputs.bam_compression)', ' ')))  $(defHandler('-baq', WDLCommandPart('NonNull(inputs.baq)', 'OFF')))  $(defHandler('-baqGOP', WDLCommandPart('NonNull(inputs.baqGapOpenPenalty)', '40.0')))  $(defHandler('-BQSR', WDLCommandPart('NonNull(inputs.BQSR)', ' ')))  $(defHandler('-DBQ', WDLCommandPart('NonNull(inputs.defaultBaseQualities)', '-1')))  $(defHandler('-disable_auto_index_creation_and_locking_when_reading_rods', WDLCommandPart('NonNull(inputs.disable_auto_index_creation_and_locking_when_reading_rods)', 'false')))  $(defHandler('NA', WDLCommandPart('NonNull(inputs.disable_bam_indexing)', 'false')))  $(defHandler('-DIQ', WDLCommandPart('NonNull(inputs.disable_indel_quals)', 'false')))  $(defHandler('-drf', WDLCommandPart('NonNull(inputs.disable_read_filter)', '[]')))  $(defHandler('-dcov', WDLCommandPart('NonNull(inputs.downsample_to_coverage)', ' ')))  $(defHandler('-dfrac', WDLCommandPart('NonNull(inputs.downsample_to_fraction)', ' ')))  $(defHandler('-dt', WDLCommandPart('NonNull(inputs.downsampling_type)', ' ')))  $(defHandler('-EOQ', WDLCommandPart('NonNull(inputs.emit_original_quals)', 'false')))  $(defHandler('-XL', WDLCommandPart('NonNull(inputs.excludeIntervals)', ' ')))  $(defHandler('-fixMisencodedQuals', WDLCommandPart('NonNull(inputs.fix_misencoded_quality_scores)', 'false')))  $(defHandler('NA', WDLCommandPart('NonNull(inputs.generate_md5)', 'false')))  $(defHandler('-globalQScorePrior', WDLCommandPart('NonNull(inputs.globalQScorePrior)', '-1.0')))  $(defHandler('-h', WDLCommandPart('NonNull(inputs.help)', 'false')))  $(defHandler('-I', WDLCommandPart('NonNull(inputs.input_file)', '[]')))  $(defHandler('-im', WDLCommandPart('NonNull(inputs.interval_merging)', 'ALL')))  $(defHandler('-ip', WDLCommandPart('NonNull(inputs.interval_padding)', '0')))  $(defHandler('-isr', WDLCommandPart('NonNull(inputs.interval_set_rule)', 'UNION')))  $(defHandler('-L', WDLCommandPart('NonNull(inputs.intervals)', ' ')))  $(defHandler('-kpr', WDLCommandPart('NonNull(inputs.keep_program_records)', 'false')))  $(defHandler('-log', WDLCommandPart('NonNull(inputs.log_to_file)', ' ')))  $(defHandler('-l', WDLCommandPart('NonNull(inputs.logging_level)', 'INFO')))  $(defHandler('-maxRuntime', WDLCommandPart('NonNull(inputs.maxRuntime)', '-1')))  $(defHandler('-maxRuntimeUnits', WDLCommandPart('NonNull(inputs.maxRuntimeUnits)', 'MINUTES')))  $(defHandler('-mte', WDLCommandPart('NonNull(inputs.monitorThreadEfficiency)', 'false')))  $(defHandler('-writeFullFormat', WDLCommandPart('NonNull(inputs.never_trim_vcf_format_field)', 'false')))  $(defHandler('-no_cmdline_in_header', WDLCommandPart('NonNull(inputs.no_cmdline_in_header)', 'false')))  $(defHandler('-ndrs', WDLCommandPart('NonNull(inputs.nonDeterministicRandomSeed)', 'false')))  $(defHandler('-nct', WDLCommandPart('NonNull(inputs.num_cpu_threads_per_data_thread)', '1')))  $(defHandler('-nt', WDLCommandPart('NonNull(inputs.num_threads)', '1')))  $(defHandler('-ped', WDLCommandPart('NonNull(inputs.pedigree)', '[]')))  $(defHandler('-pedString', WDLCommandPart('NonNull(inputs.pedigreeString)', '[]')))  $(defHandler('-pedValidationType', WDLCommandPart('NonNull(inputs.pedigreeValidationType)', 'STRICT')))  $(defHandler('-PF', WDLCommandPart('NonNull(inputs.performanceLog)', ' ')))  $(defHandler('-preserveQ', WDLCommandPart('NonNull(inputs.preserve_qscores_less_than)', '6')))  $(defHandler('-qq', WDLCommandPart('NonNull(inputs.quantize_quals)', '0')))  $(defHandler('-rbs', WDLCommandPart('NonNull(inputs.read_buffer_size)', ' ')))  $(defHandler('-rf', WDLCommandPart('NonNull(inputs.read_filter)', '[]')))  $(defHandler('-rgbl', WDLCommandPart('NonNull(inputs.read_group_black_list)', ' ')))  $(defHandler('-fixNDN', WDLCommandPart('NonNull(inputs.refactor_NDN_cigar_string)', 'false')))  $(defHandler('-R', WDLCommandPart('NonNull(inputs.reference_sequence)', ' ')))  $(defHandler('-ref_win_stop', WDLCommandPart('NonNull(inputs.reference_window_stop)', '0')))  $(defHandler('-rpr', WDLCommandPart('NonNull(inputs.remove_program_records)', 'false')))  $(defHandler('-sample_rename_mapping_file', WDLCommandPart('NonNull(inputs.sample_rename_mapping_file)', ' ')))  $(defHandler('-secondsBetweenProgressUpdates', WDLCommandPart('NonNull(inputs.secondsBetweenProgressUpdates)', '10')))  $(defHandler('NA', WDLCommandPart('NonNull(inputs.showFullBamList)', 'false')))  $(defHandler('-simplifyBAM', WDLCommandPart('NonNull(inputs.simplifyBAM)', 'false')))  $(defHandler('-sites_only', WDLCommandPart('NonNull(inputs.sites_only)', 'false')))  $(defHandler('-SQQ', WDLCommandPart('NonNull(inputs.static_quantized_quals)', ' ')))  $(defHandler('-U', WDLCommandPart('NonNull(inputs.unsafe)', ' ')))  $(defHandler('-OQ', WDLCommandPart('NonNull(inputs.useOriginalQualities)', 'false')))  $(defHandler('-S', WDLCommandPart('NonNull(inputs.validation_strictness)', 'SILENT')))  $(defHandler('-variant_index_parameter', WDLCommandPart('NonNull(inputs.variant_index_parameter)', '-1')))  $(defHandler('-variant_index_type', WDLCommandPart('NonNull(inputs.variant_index_type)', 'DYNAMIC_SEEK')))  $(defHandler('-version', WDLCommandPart('NonNull(inputs.version)', 'false')))"
        }
    ], 
    "class": "CommandLineTool"
}