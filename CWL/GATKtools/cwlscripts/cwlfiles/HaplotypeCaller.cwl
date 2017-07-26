{
    "cwlVersion": "v1.0", 
    "inputs": [
        {
            "doc": "Reference sequence file", 
            "type": "File?", 
            "id": "reference_sequence", 
            "secondaryFiles": [
                ".fai", 
                "^.dict"
            ]
        }, 
        {
            "doc": "Input file containing sequence data (BAM or CRAM)", 
            "type": "File", 
            "id": "input_file", 
            "secondaryFiles": "$(self.location+'.'+self.basename.split('.').splice(-1)[0].replace('m','i'))"
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
            "doc": "Threshold for the probability of a profile state being active.", 
            "type": "double?", 
            "id": "activeProbabilityThreshold"
        }, 
        {
            "doc": "The active region extension; if not provided defaults to Walker annotated default", 
            "type": "int?", 
            "id": "activeRegionExtension"
        }, 
        {
            "doc": "Use this interval list file as the active regions to process", 
            "type": [
                "string[]?", 
                "File"
            ], 
            "id": "activeRegionIn"
        }, 
        {
            "doc": "The active region maximum size; if not provided defaults to Walker annotated default", 
            "type": "int?", 
            "id": "activeRegionMaxSize"
        }, 
        {
            "doc": "Output the active region to this IGV formatted file", 
            "type": "null?", 
            "id": "activeRegionOut"
        }, 
        {
            "doc": "Output the raw activity profile results in IGV format", 
            "type": "null?", 
            "id": "activityProfileOut"
        }, 
        {
            "doc": "The set of alleles at which to genotype when --genotyping_mode is GENOTYPE_GIVEN_ALLELES", 
            "type": "File?", 
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
            "doc": "If provided, we will annotate records with the number of alternate alleles that were discovered (but not necessarily genotyped) at a given site", 
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
            "type": {
                "symbols": [
                    "ALL_POSSIBLE_HAPLOTYPES", 
                    "CALLED_HAPLOTYPES"
                ], 
                "type": "enum?"
            }, 
            "id": "bamWriterType"
        }, 
        {
            "doc": "The sigma of the band pass filter Gaussian kernel; if not provided defaults to Walker annotated default", 
            "type": "double?", 
            "id": "bandPassSigma"
        }, 
        {
            "doc": "Comparison VCF file", 
            "type": "File[]?", 
            "id": "comp"
        }, 
        {
            "doc": "1000G consensus mode", 
            "type": "boolean?", 
            "id": "consensus"
        }, 
        {
            "doc": "Tab-separated File containing fraction of contamination in sequencing data (per sample) to aggressively remove. Format should be \"<SampleID><TAB><Contamination>\" (Contamination is double) per line; No header.", 
            "type": "File?", 
            "id": "contamination_fraction_per_sample_file"
        }, 
        {
            "doc": "Fraction of contamination in sequencing data (for all samples) to aggressively remove", 
            "type": "double?", 
            "id": "contamination_fraction_to_filter"
        }, 
        {
            "doc": "dbSNP file", 
            "type": "File?", 
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
            "doc": "Mode for emitting reference confidence scores", 
            "type": {
                "symbols": [
                    "NONE", 
                    "BP_RESOLUTION", 
                    "GVCF"
                ], 
                "type": "enum?"
            }, 
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
            "type": "int?", 
            "id": "gcpHMM"
        }, 
        {
            "doc": "Specifies how to determine the alternate alleles to use for genotyping", 
            "type": {
                "symbols": [
                    "DISCOVERY", 
                    "GENOTYPE_GIVEN_ALLELES"
                ], 
                "type": "enum?"
            }, 
            "id": "genotyping_mode"
        }, 
        {
            "doc": "Write debug assembly graph information to this file", 
            "type": "null?", 
            "id": "graphOutput"
        }, 
        {
            "doc": "One or more classes/groups of annotations to apply to variant calls", 
            "type": "string[]?", 
            "id": "group"
        }, 
        {
            "doc": "GQ thresholds for reference confidence bands", 
            "type": "int[]?", 
            "id": "GVCFGQBands"
        }, 
        {
            "doc": "Heterozygosity value used to compute prior likelihoods for any locus", 
            "type": "double?", 
            "id": "heterozygosity"
        }, 
        {
            "doc": "Heterozygosity for indel calling", 
            "type": "double?", 
            "id": "indel_heterozygosity"
        }, 
        {
            "doc": "The size of an indel to check for in the reference model", 
            "type": "int?", 
            "id": "indelSizeToEliminateInRefModel"
        }, 
        {
            "doc": "Input prior for calls", 
            "type": "double[]?", 
            "id": "input_prior"
        }, 
        {
            "doc": "Kmer size to use in the read threading assembler", 
            "type": "int[]?", 
            "id": "kmerSize"
        }, 
        {
            "doc": "Maximum number of alternate alleles to genotype", 
            "type": "int?", 
            "id": "max_alternate_alleles"
        }, 
        {
            "doc": "Maximum number of haplotypes to consider for your population", 
            "type": "int?", 
            "id": "maxNumHaplotypesInPopulation"
        }, 
        {
            "doc": "Maximum reads in an active region", 
            "type": "int?", 
            "id": "maxReadsInRegionPerSample"
        }, 
        {
            "doc": "Minimum base quality required to consider a base for calling", 
            "type": "int?", 
            "id": "min_base_quality_score"
        }, 
        {
            "doc": "Minimum length of a dangling branch to attempt recovery", 
            "type": "int?", 
            "id": "minDanglingBranchLength"
        }, 
        {
            "doc": "Minimum support to not prune paths in the graph", 
            "type": "int?", 
            "id": "minPruning"
        }, 
        {
            "doc": "Minimum number of reads sharing the same alignment start for each genomic location in an active region", 
            "type": "int?", 
            "id": "minReadsPerAlignmentStart"
        }, 
        {
            "doc": "Number of samples that must pass the minPruning threshold", 
            "type": "int?", 
            "id": "numPruningSamples"
        }, 
        {
            "doc": "File to which variants should be written", 
            "type": "string?", 
            "id": "out"
        }, 
        {
            "doc": "Specifies which type of calls we should output", 
            "type": {
                "symbols": [
                    "EMIT_VARIANTS_ONLY", 
                    "EMIT_ALL_CONFIDENT_SITES", 
                    "EMIT_ALL_SITES"
                ], 
                "type": "enum?"
            }, 
            "id": "output_mode"
        }, 
        {
            "doc": "The PCR indel model to use", 
            "type": {
                "symbols": [
                    "NONE", 
                    "HOSTILE", 
                    "AGGRESSIVE", 
                    "CONSERVATIVE"
                ], 
                "type": "enum?"
            }, 
            "id": "pcr_indel_model"
        }, 
        {
            "doc": "The global assumed mismapping rate for reads", 
            "type": "int?", 
            "id": "phredScaledGlobalReadMismappingRate"
        }, 
        {
            "doc": "Name of single sample to use from a multi-sample bam", 
            "type": "string?", 
            "id": "sample_name"
        }, 
        {
            "doc": "Ploidy (number of chromosomes) per sample. For pooled data, set to (Number of samples in each pool * Sample Ploidy).", 
            "type": "int?", 
            "id": "sample_ploidy"
        }, 
        {
            "doc": "The minimum phred-scaled confidence threshold at which variants should be called", 
            "type": "double?", 
            "id": "standard_min_confidence_threshold_for_calling"
        }, 
        {
            "doc": "The minimum phred-scaled confidence threshold at which variants should be emitted (and filtered with LowQual if less than the calling threshold)", 
            "type": "double?", 
            "id": "standard_min_confidence_threshold_for_emitting"
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
            "type": {
                "symbols": [
                    "OFF", 
                    "CALCULATE_AS_NECESSARY", 
                    "RECALCULATE"
                ], 
                "type": "enum?"
            }, 
            "id": "baq"
        }, 
        {
            "doc": "BAQ gap open penalty", 
            "type": "double?", 
            "id": "baqGapOpenPenalty"
        }, 
        {
            "doc": "Input covariates table file for on-the-fly base quality score recalibration", 
            "type": "File?", 
            "id": "BQSR"
        }, 
        {
            "doc": "Disable both auto-generation of index files and index file locking", 
            "type": "boolean?", 
            "id": "disable_auto_index_creation_and_locking_when_reading_rods"
        }, 
        {
            "doc": "Turn off on-the-fly creation of indices for output BAM/CRAM files.", 
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
            "type": "double?", 
            "id": "downsample_to_fraction"
        }, 
        {
            "doc": "Type of read downsampling to employ at a given locus", 
            "type": {
                "symbols": [
                    "NONE", 
                    "ALL_READS", 
                    "BY_SAMPLE"
                ], 
                "type": "enum?"
            }, 
            "id": "downsampling_type"
        }, 
        {
            "doc": "Emit the OQ tag with the original base qualities (with -BQSR)", 
            "type": "boolean?", 
            "id": "emit_original_quals"
        }, 
        {
            "doc": "One or more genomic intervals to exclude from processing", 
            "type": [
                "string[]?", 
                "File"
            ], 
            "id": "excludeIntervals"
        }, 
        {
            "doc": "Fix mis-encoded base quality scores", 
            "type": "boolean?", 
            "id": "fix_misencoded_quality_scores"
        }, 
        {
            "doc": "GATK key file required to run with -et NO_ET", 
            "type": "File?", 
            "id": "gatk_key"
        }, 
        {
            "doc": "Enable on-the-fly creation of md5s for output BAM files.", 
            "type": "boolean?", 
            "id": "generate_md5"
        }, 
        {
            "doc": "Global Qscore Bayesian prior to use for BQSR", 
            "type": "double?", 
            "id": "globalQScorePrior"
        }, 
        {
            "doc": "Interval merging rule for abutting intervals", 
            "type": {
                "symbols": [
                    "ALL", 
                    "OVERLAPPING_ONLY"
                ], 
                "type": "enum?"
            }, 
            "id": "interval_merging"
        }, 
        {
            "doc": "Amount of padding (in bp) to add to each interval", 
            "type": "int?", 
            "id": "interval_padding"
        }, 
        {
            "doc": "Set merging approach to use for combining interval inputs", 
            "type": {
                "symbols": [
                    "UNION", 
                    "INTERSECTION"
                ], 
                "type": "enum?"
            }, 
            "id": "interval_set_rule"
        }, 
        {
            "doc": "One or more genomic intervals over which to operate", 
            "type": [
                "string[]?", 
                "File"
            ], 
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
            "type": "long?", 
            "id": "maxRuntime"
        }, 
        {
            "doc": "Unit of time used by maxRuntime", 
            "type": {
                "symbols": [
                    "NANOSECONDS", 
                    "MICROSECONDS", 
                    "MILLISECONDS", 
                    "SECONDS", 
                    "MINUTES", 
                    "HOURS", 
                    "DAYS"
                ], 
                "type": "enum?"
            }, 
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
            "doc": "Use a non-deterministic random seed", 
            "type": "boolean?", 
            "id": "nonDeterministicRandomSeed"
        }, 
        {
            "doc": "Number of CPU threads to allocate per data thread", 
            "type": "int?", 
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
            "doc": "Validation strictness for pedigree information", 
            "type": {
                "symbols": [
                    "STRICT", 
                    "SILENT"
                ], 
                "type": "enum?"
            }, 
            "id": "pedigreeValidationType"
        }, 
        {
            "doc": "Write GATK runtime performance log to this file", 
            "type": "File?", 
            "id": "performanceLog"
        }, 
        {
            "doc": "Run reporting mode", 
            "type": {
                "symbols": [
                    "NO_ET", 
                    "AWS", 
                    "STDOUT"
                ], 
                "type": "enum?"
            }, 
            "id": "phone_home"
        }, 
        {
            "doc": "Don't recalibrate bases with quality scores less than this threshold (with -BQSR)", 
            "type": "int?", 
            "id": "preserve_qscores_less_than"
        }, 
        {
            "doc": "Quantize quality scores to a given number of levels (with -BQSR)", 
            "type": "int?", 
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
            "doc": "Reference window stop", 
            "type": "int?", 
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
            "doc": "Emit a log entry (level INFO) containing the full list of sequence data files to be included in the analysis (including files inside .bam.list or .cram.list files).", 
            "type": "boolean?", 
            "id": "showFullBamList"
        }, 
        {
            "doc": "If provided, output BAM/CRAM files will be simplified to include just key reads for downstream variation discovery analyses (removing duplicates, PF-, non-primary reads), as well stripping all extended tags from the kept reads except the read group identifier", 
            "type": "boolean?", 
            "id": "simplifyBAM"
        }, 
        {
            "doc": "Just output sites without genotypes (i.e. only the first 8 columns of the VCF)", 
            "type": "boolean?", 
            "id": "sites_only"
        }, 
        {
            "doc": "Use static quantized quality scores to a given number of levels (with -BQSR)", 
            "type": "int[]?", 
            "id": "static_quantized_quals"
        }, 
        {
            "doc": "Tag to identify this GATK run as part of a group of runs", 
            "type": "string?", 
            "id": "tag"
        }, 
        {
            "doc": "Enable unsafe operations: nothing will be checked at runtime", 
            "type": {
                "symbols": [
                    "ALLOW_N_CIGAR_READS", 
                    "ALLOW_UNINDEXED_BAM", 
                    "ALLOW_UNSET_BAM_SORT_ORDER", 
                    "NO_READ_ORDER_VERIFICATION", 
                    "ALLOW_SEQ_DICT_INCOMPATIBILITY", 
                    "LENIENT_VCF_PROCESSING", 
                    "ALL"
                ], 
                "type": "enum?"
            }, 
            "id": "unsafe"
        }, 
        {
            "doc": "Use the base quality scores from the OQ tag", 
            "type": "boolean?", 
            "id": "useOriginalQualities"
        }, 
        {
            "doc": "How strict should we be with validation", 
            "type": {
                "symbols": [
                    "STRICT", 
                    "LENIENT", 
                    "SILENT"
                ], 
                "type": "enum?"
            }, 
            "id": "validation_strictness"
        }, 
        {
            "doc": "Parameter to pass to the VCF/BCF IndexCreator", 
            "type": "int?", 
            "id": "variant_index_parameter"
        }, 
        {
            "doc": "Type of IndexCreator to use for VCF/BCF indices", 
            "type": {
                "symbols": [
                    "DYNAMIC_SEEK", 
                    "DYNAMIC_SIZE", 
                    "LINEAR", 
                    "INTERVAL"
                ], 
                "type": "enum?"
            }, 
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
                "function WDLCommandPart(expr, def) {var rval; try { rval = eval(expr);} catch(err) {rval = def;} return rval;}", 
                "function NonNull(x) {if(x === null || x == 'NA') {throw new UserException('NullValue');} else {return x;}}", 
                "function defHandler (com, def) {if(Array.isArray(def) && def.length == 0) {return '';} \n                                              else if(Array.isArray(def) && def.length !=0 ) {return def.map(element => com+ ' ' + element).join(' ');}\n                                              else if (def =='false') {return '';} else if (def == 'true') {return com;} \n                                              if (def == []) {return '';} else {return com + ' ' + def;}}", 
                "function secondaryfiles(f) { return typeof f; }"
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
                "glob": "$(inputs.bamOutput)"
            }, 
            "type": [
                "null", 
                "File"
            ], 
            "id": "--bamOutput"
        }, 
        {
            "outputBinding": {
                "glob": "$(inputs.out)"
            }, 
            "type": [
                "null", 
                "File"
            ], 
            "id": "--out"
        }
    ], 
    "baseCommand": [], 
    "id": "HaplotypeCaller", 
    "arguments": [
        {
            "shellQuote": false, 
            "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar  -ActProbThresh $(WDLCommandPart('NonNull(inputs.activeProbabilityThreshold)', '0.002')) $(WDLCommandPart('-activeRegionExtension  NonNull(inputs.activeRegionExtension)', ' ')) $(defHandler('-AR', WDLCommandPart('NonNull(inputs.activeRegionIn)', []))) $(WDLCommandPart('-activeRegionMaxSize  NonNull(inputs.activeRegionMaxSize)', ' ')) $(WDLCommandPart('-ARO  NonNull(inputs.activeRegionOut)', ' ')) $(WDLCommandPart('-APO  NonNull(inputs.activityProfileOut)', ' ')) $(WDLCommandPart('-alleles  NonNull(inputs.alleles)', ' ')) $(WDLCommandPart('-allowNonUniqueKmersInRef  NonNull(inputs.allowNonUniqueKmersInRef)', ' ')) $(WDLCommandPart('-allSitePLs  NonNull(inputs.allSitePLs)', ' ')) $(WDLCommandPart('-nda  NonNull(inputs.annotateNDA)', ' ')) $(defHandler('-A', WDLCommandPart('NonNull(inputs.annotation)', []))) $(WDLCommandPart('-bamout  NonNull(inputs.bamOutput.path)', ' ')) $(WDLCommandPart('-bamWriterType  NonNull(inputs.bamWriterType)', ' ')) $(WDLCommandPart('-bandPassSigma  NonNull(inputs.bandPassSigma)', ' ')) $(defHandler('-comp', WDLCommandPart('NonNull(inputs.comp)', []))) $(WDLCommandPart('-consensus  NonNull(inputs.consensus)', ' ')) $(WDLCommandPart('-contaminationFile  NonNull(inputs.contamination_fraction_per_sample_file.path)', ' ')) -contamination $(WDLCommandPart('NonNull(inputs.contamination_fraction_to_filter)', '0.0')) $(WDLCommandPart('-D  NonNull(inputs.dbsnp)', ' ')) $(WDLCommandPart('-debug  NonNull(inputs.debug)', ' ')) $(WDLCommandPart('-disableOptimizations  NonNull(inputs.disableOptimizations)', ' ')) $(WDLCommandPart('-doNotRunPhysicalPhasing  NonNull(inputs.doNotRunPhysicalPhasing)', ' ')) $(WDLCommandPart('-dontIncreaseKmerSizesForCycles  NonNull(inputs.dontIncreaseKmerSizesForCycles)', ' ')) $(WDLCommandPart('-dontTrimActiveRegions  NonNull(inputs.dontTrimActiveRegions)', ' ')) $(WDLCommandPart('-dontUseSoftClippedBases  NonNull(inputs.dontUseSoftClippedBases)', ' ')) $(WDLCommandPart('-ERC  NonNull(inputs.emitRefConfidence)', ' ')) $(defHandler('-XA', WDLCommandPart('NonNull(inputs.excludeAnnotation)', []))) $(WDLCommandPart('-forceActive  NonNull(inputs.forceActive)', ' ')) -gcpHMM $(WDLCommandPart('NonNull(inputs.gcpHMM)', '10')) $(WDLCommandPart('-gt_mode  NonNull(inputs.genotyping_mode)', ' ')) $(WDLCommandPart('-graph  NonNull(inputs.graphOutput)', ' ')) $(defHandler('-G', WDLCommandPart('NonNull(inputs.group)', []))) $(defHandler('-GQB', WDLCommandPart('NonNull(inputs.GVCFGQBands)', []))) -hets $(WDLCommandPart('NonNull(inputs.heterozygosity)', '0.001')) -indelHeterozygosity $(WDLCommandPart('NonNull(inputs.indel_heterozygosity)', '1.25E-4')) -ERCIS $(WDLCommandPart('NonNull(inputs.indelSizeToEliminateInRefModel)', '10')) $(defHandler('-inputPrior', WDLCommandPart('NonNull(inputs.input_prior)', []))) $(defHandler('-kmerSize', WDLCommandPart('NonNull(inputs.kmerSize)', []))) -maxAltAlleles $(WDLCommandPart('NonNull(inputs.max_alternate_alleles)', '6')) -maxNumHaplotypesInPopulation $(WDLCommandPart('NonNull(inputs.maxNumHaplotypesInPopulation)', '128')) -maxReadsInRegionPerSample $(WDLCommandPart('NonNull(inputs.maxReadsInRegionPerSample)', '10000')) -mbq $(WDLCommandPart('NonNull(inputs.min_base_quality_score)', '10')) -minDanglingBranchLength $(WDLCommandPart('NonNull(inputs.minDanglingBranchLength)', '4')) -minPruning $(WDLCommandPart('NonNull(inputs.minPruning)', '2')) -minReadsPerAlignStart $(WDLCommandPart('NonNull(inputs.minReadsPerAlignmentStart)', '10')) -numPruningSamples $(WDLCommandPart('NonNull(inputs.numPruningSamples)', '1')) $(defHandler('-o', WDLCommandPart('NonNull(inputs.out)', 'stdout'))) $(WDLCommandPart('-out_mode  NonNull(inputs.output_mode)', ' ')) $(WDLCommandPart('-pcrModel  NonNull(inputs.pcr_indel_model)', ' ')) -globalMAPQ $(WDLCommandPart('NonNull(inputs.phredScaledGlobalReadMismappingRate)', '45')) $(WDLCommandPart('-sn  NonNull(inputs.sample_name)', ' ')) -ploidy $(WDLCommandPart('NonNull(inputs.sample_ploidy)', '2')) -stand_call_conf $(WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_calling)', '30.0')) -stand_emit_conf $(WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_emitting)', '30.0')) $(WDLCommandPart('-allelesTrigger  NonNull(inputs.useAllelesTrigger)', ' ')) $(WDLCommandPart('-useFilteredReadsForAnnotations  NonNull(inputs.useFilteredReadsForAnnotations)', ' ')) $(WDLCommandPart('-allowPotentiallyMisencodedQuals  NonNull(inputs.allow_potentially_misencoded_quality_scores)', ' ')) -T $(inputs.analysis_type)$(WDLCommandPart('-compress  NonNull(inputs.bam_compression)', ' ')) $(WDLCommandPart('-baq  NonNull(inputs.baq)', ' ')) -baqGOP $(WDLCommandPart('NonNull(inputs.baqGapOpenPenalty)', '40.0')) $(WDLCommandPart('-BQSR  NonNull(inputs.BQSR.path)', ' ')) $(WDLCommandPart('-disable_auto_index_creation_and_locking_when_reading_rods  NonNull(inputs.disable_auto_index_creation_and_locking_when_reading_rods)', ' ')) $(WDLCommandPart('NA  NonNull(inputs.disable_bam_indexing)', ' ')) $(WDLCommandPart('-DIQ  NonNull(inputs.disable_indel_quals)', ' ')) $(defHandler('-drf', WDLCommandPart('NonNull(inputs.disable_read_filter)', []))) $(WDLCommandPart('-dcov  NonNull(inputs.downsample_to_coverage)', ' ')) $(WDLCommandPart('-dfrac  NonNull(inputs.downsample_to_fraction)', ' ')) $(WDLCommandPart('-dt  NonNull(inputs.downsampling_type)', ' ')) $(WDLCommandPart('-EOQ  NonNull(inputs.emit_original_quals)', ' ')) $(defHandler('-XL', WDLCommandPart('NonNull(inputs.excludeIntervals)', []))) $(WDLCommandPart('-fixMisencodedQuals  NonNull(inputs.fix_misencoded_quality_scores)', ' ')) $(WDLCommandPart('-K  NonNull(inputs.gatk_key.path)', ' ')) $(WDLCommandPart('NA  NonNull(inputs.generate_md5)', ' ')) -globalQScorePrior $(WDLCommandPart('NonNull(inputs.globalQScorePrior)', '-1.0')) -I $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) $(WDLCommandPart('-im  NonNull(inputs.interval_merging)', ' ')) -ip $(WDLCommandPart('NonNull(inputs.interval_padding)', '0')) $(WDLCommandPart('-isr  NonNull(inputs.interval_set_rule)', ' ')) $(defHandler('-L', WDLCommandPart('NonNull(inputs.intervals)', []))) $(WDLCommandPart('-kpr  NonNull(inputs.keep_program_records)', ' ')) $(WDLCommandPart('-log  NonNull(inputs.log_to_file)', ' ')) $(WDLCommandPart('-l  NonNull(inputs.logging_level)', ' ')) -maxRuntime $(WDLCommandPart('NonNull(inputs.maxRuntime)', '-1')) $(WDLCommandPart('-maxRuntimeUnits  NonNull(inputs.maxRuntimeUnits)', ' ')) $(WDLCommandPart('-mte  NonNull(inputs.monitorThreadEfficiency)', ' ')) $(WDLCommandPart('-writeFullFormat  NonNull(inputs.never_trim_vcf_format_field)', ' ')) $(WDLCommandPart('-ndrs  NonNull(inputs.nonDeterministicRandomSeed)', ' ')) -nct $(WDLCommandPart('NonNull(inputs.num_cpu_threads_per_data_thread)', '1')) -nt $(WDLCommandPart('NonNull(inputs.num_threads)', '1')) $(defHandler('-ped', WDLCommandPart('NonNull(inputs.pedigree)', []))) $(defHandler('-pedString', WDLCommandPart('NonNull(inputs.pedigreeString)', []))) $(WDLCommandPart('-pedValidationType  NonNull(inputs.pedigreeValidationType)', ' ')) $(WDLCommandPart('-PF  NonNull(inputs.performanceLog.path)', ' ')) $(WDLCommandPart('-et  NonNull(inputs.phone_home)', ' ')) -preserveQ $(WDLCommandPart('NonNull(inputs.preserve_qscores_less_than)', '6')) -qq $(WDLCommandPart('NonNull(inputs.quantize_quals)', '0')) $(WDLCommandPart('-rbs  NonNull(inputs.read_buffer_size)', ' ')) $(defHandler('-rf', WDLCommandPart('NonNull(inputs.read_filter)', []))) $(defHandler('-rgbl', WDLCommandPart('NonNull(inputs.read_group_black_list)', []))) $(WDLCommandPart('-fixNDN  NonNull(inputs.refactor_NDN_cigar_string)', ' ')) -R $(WDLCommandPart('NonNull(inputs.reference_sequence.path)', '')) -ref_win_stop $(WDLCommandPart('NonNull(inputs.reference_window_stop)', '0')) $(WDLCommandPart('-rpr  NonNull(inputs.remove_program_records)', ' ')) $(WDLCommandPart('-sample_rename_mapping_file  NonNull(inputs.sample_rename_mapping_file.path)', ' ')) $(WDLCommandPart('NA  NonNull(inputs.showFullBamList)', ' ')) $(WDLCommandPart('-simplifyBAM  NonNull(inputs.simplifyBAM)', ' ')) $(WDLCommandPart('-sites_only  NonNull(inputs.sites_only)', ' ')) $(defHandler('-SQQ', WDLCommandPart('NonNull(inputs.static_quantized_quals)', []))) $(WDLCommandPart('-tag  NonNull(inputs.tag)', ' ')) $(WDLCommandPart('-U  NonNull(inputs.unsafe)', ' ')) $(WDLCommandPart('-OQ  NonNull(inputs.useOriginalQualities)', ' ')) $(WDLCommandPart('-S  NonNull(inputs.validation_strictness)', ' ')) -variant_index_parameter $(WDLCommandPart('NonNull(inputs.variant_index_parameter)', '-1')) $(WDLCommandPart('-variant_index_type  NonNull(inputs.variant_index_type)', ' ')) $(WDLCommandPart('-version  NonNull(inputs.version)', ' ')) "
        }
    ], 
    "class": "CommandLineTool"
}