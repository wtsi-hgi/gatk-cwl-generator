#!/usr/bin/env cwl-runner
# This tool description was generated automatically by wdl2cwl ver. 0.2

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
            "id": "refIndex",
#            "secondaryFiles": ".fai"
        }, 
        {
            "doc": "dict file of reference genome", 
            "type": "File", 
            "id": "refDict"
        }, 
        {
            "doc": "An optional parameter which allows the user to specify additions to the command line at run time", 
            "type": "string?", 
            "id": "userString"
        }, 
        {
            "doc": "Input file containing sequence data (BAM or CRAM)", 
            "type": "File", 
            "id": "input_file",
            "secondaryFiles": [
                  ".crai",
                  "^.dict"
            ]
        }, 
        {
            "doc": "One or more genomic intervals over which to operate", 
            "type": "string[]?", 
            "id": "intervals"
        }, 
        {
            "doc": "Input covariates table file for on-the-fly base quality score recalibration", 
            "type": "File?", 
            "id": "BQSR"
        }, 
        {
            "type": "int?", 
            "id": "nctVal"
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
            "doc": "The set of alleles at which to genotype when --genotyping_mode is GENOTYPE_GIVEN_ALLELES", 
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
            "doc": "Tab-separated File containing fraction of contamination in sequencing data (per sample) to aggressively remove. Format should be <SampleID><TAB><Contamination> (Contamination is double) per line; No header.", 
            "type": "File?", 
            "id": "contamination_fraction_per_sample_file"
        }, 
        {
            "doc": "Fraction of contamination in sequencing data (for all samples) to aggressively remove", 
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
            "doc": "Emit reads that are dropped for filtering, trimming, realignment failure -edr $(WDLCommandPart('NonNull(inputs.emitDroppedReads)', 'false'))", 
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
            "type": "int?", 
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
            "doc": "GQ thresholds for reference confidence bands", 
            "type": "int[]?", 
            "id": "GVCFGQBands"
        }, 
        {
            "doc": "Heterozygosity value used to compute prior likelihoods for any locus", 
            "type": "float?", 
            "id": "heterozygosity"
        }, 
        {
            "doc": "Heterozygosity for indel calling", 
            "type": "float?", 
            "id": "indel_heterozygosity"
        }, 
        {
            "doc": "The size of an indel to check for in the reference model", 
            "type": "int?", 
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
            "type": "int?", 
            "id": "max_alternate_alleles"
        }, 
        {
            "doc": "Maximum number of PL values to output -maxNumPLValues $(WDLCommandPart('NonNull(inputs.max_num_PL_values)', '100')) ", 
            "type": "int?", 
            "id": "max_num_PL_values"
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
            "type": "string?", 
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
            "type": "string", 
            "id": "out"
        }, 
        {
            "doc": "Specifies which type of calls we should output", 
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
            "type": "float?", 
            "id": "standard_min_confidence_threshold_for_calling"
        }, 
        {
            "doc": "The minimum phred-scaled confidence threshold at which variants should be emitted (and filtered with LowQual if less than the calling threshold)", 
            "type": "float?", 
            "id": "standard_min_confidence_threshold_for_emitting"
        }, 
        {
            "doc": "Use additional trigger on variants found in an external alleles file", 
            "type": "boolean?", 
            "id": "useAllelesTrigger"
        }, 
        {
            "doc": "Use the contamination-filtered read maps for the purposes of annotating variants console.log('hello world'); console.log('Is array = %j def=%j self=%j inputs=%j', Array.isArray(def), def, self, inputs);   {if(Array.isArray(def)) {return 'ARRAY';} else {return 'NOT'} }", 
            "type": "boolean?", 
            "id": "useFilteredReadsForAnnotations"
        }
    ], 
    "requirements": [
        {
            "class": "ShellCommandRequirement"
        }, 
        {
            "class": "InlineJavascriptRequirement", 
            "expressionLib": [
                "function WDLCommandPart(expr, def) {var rval; try {rval = eval(expr);} catch(err) { rval = def;} return rval;}",
                "function NonNull(x) {if(x === null) {throw new UserException(\"NullValue\");} else { return x; }}",
                "function defHandler (com, def) {if(Array.isArray(def) && def.length == 0) {return '';} else if(Array.isArray(def) && def.length !=0) {return def.map(element => com + ' ' + element).join(' ');} else if (def == \"false\") {return \"\";} else if (def == \"true\") {return com;} if (def == []) {return \"\";} else {return com + def;} }"
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
    "class": "CommandLineTool", 
    "arguments": [
        {
            "shellQuote": false, 
            "valueFrom": "java -jar /gatk/GenomeAnalysisTK.jar -T HaplotypeCaller -R $(WDLCommandPart('NonNull(inputs.ref.path)', '')) --input_file $(WDLCommandPart('NonNull(inputs.input_file.path)', '')) $(WDLCommandPart('\"--intervals \" + NonNull(inputs.intervals)', '')) $(WDLCommandPart('\"--BQSR \" + NonNull(inputs.BQSR)', '')) $(WDLCommandPart('\"-nct\" + NonNull(inputs.nctVal)', '')) $(defHandler('-ActProbThresh', WDLCommandPart('NonNull(inputs.activeProbabilityThreshold)', '0.002')))  $(defHandler('-activeRegionExtension', WDLCommandPart('NonNull(inputs.activeRegionExtension)', ' '))) $(WDLCommandPart('\"-AR \" + NonNull(inputs.activeRegionIn)', '')) $(WDLCommandPart('\"-activeRegionMaxSize \" + NonNull(inputs.activeRegionMaxSize)', '')) $(WDLCommandPart('\"-ARO \" + NonNull(inputs.activeRegionOut)', '')) $(WDLCommandPart('\"-APO \" + NonNull(inputs.activityProfileOut)', '')) $(WDLCommandPart('\"-alleles \" + NonNull(inputs.alleles)', '')) $(defHandler('-allowNonUniqueKmersInRef', WDLCommandPart('NonNull(inputs.allowNonUniqueKmersInRef)', 'false'))) $(defHandler('-allSitePLs', WDLCommandPart('NonNull(inputs.allSitePLs)', 'false'))) $(defHandler('-nda', WDLCommandPart('NonNull(inputs.annotateNDA)', 'false'))) $(defHandler('-A', WDLCommandPart('NonNull(inputs.annotation)', []))) $(WDLCommandPart('\"-bamout \" + NonNull(inputs.bamOutput)', '')) -bamWriterType $(WDLCommandPart('NonNull(inputs.bamWriterType)', 'CALLED_HAPLOTYPES')) $(WDLCommandPart('\"-bandPassSigma \" + NonNull(inputs.bandPassSigma)', '')) $(defHandler('-comp', WDLCommandPart('NonNull(inputs.comp)', []))) $(defHandler('-consensus', WDLCommandPart('NonNull(inputs.consensus)', 'false'))) $(WDLCommandPart('\"-contaminationFile \" + NonNull(inputs.contamination_fraction_per_sample_file)', '')) -contamination $(WDLCommandPart('NonNull(inputs.contamination_fraction_to_filter)', '0.0')) $(WDLCommandPart('\"-D \" + NonNull(inputs.dbsnp)', '')) $(defHandler('-debug', WDLCommandPart('NonNull(inputs.debug)', 'false'))) $(defHandler('-disableOptimizations', WDLCommandPart('NonNull(inputs.disableOptimizations)', 'false'))) $(defHandler('-doNotRunPhysicalPhasing', WDLCommandPart('NonNull(inputs.doNotRunPhysicalPhasing)', 'false'))) $(defHandler('-dontIncreaseKmerSizesForCycles', WDLCommandPart('NonNull(inputs.dontIncreaseKmerSizesForCycles)', 'false'))) $(defHandler('-dontTrimActiveRegions', WDLCommandPart('NonNull(inputs.dontTrimActiveRegions)', 'false'))) $(defHandler('-dontUseSoftClippedBases', WDLCommandPart('NonNull(inputs.dontUseSoftClippedBases)', 'false'))) $(defHandler('-ERC', WDLCommandPart('NonNull(inputs.emitRefConfidence)', 'false'))) $(defHandler('-XA', WDLCommandPart('NonNull(inputs.excludeAnnotation)', []))) $(defHandler('-forceActive', WDLCommandPart('NonNull(inputs.forceActive)', 'false'))) -gcpHMM $(WDLCommandPart('NonNull(inputs.gcpHMM)', '10')) -gt_mode $(WDLCommandPart('NonNull(inputs.genotyping_mode)', 'DISCOVERY')) $(WDLCommandPart('\"-graph \" + NonNull(inputs.graphOutput)', '')) $(defHandler('-G', WDLCommandPart('NonNull(inputs.group)', ['StandardAnnotation','StandardHCAnnotation'])))  $(defHandler('-GQB', WDLCommandPart('NonNull(inputs.GVCFGQBands)', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 70, 80, 90, 99]))) -hets $(WDLCommandPart('NonNull(inputs.heterozygosity)', '0.001')) -indelHeterozygosity $(WDLCommandPart('NonNull(inputs.indel_heterozygosity)', '1.25E-4')) -ERCIS $(WDLCommandPart('NonNull(inputs.indelSizeToEliminateInRefModel)', '10')) $(defHandler('-inputPrior', WDLCommandPart('NonNull(inputs.input_prior)', [])))  $(defHandler('-kmerSize', WDLCommandPart('NonNull(inputs.kmerSize)', [10, 25]))) -maxAltAlleles $(WDLCommandPart('NonNull(inputs.max_alternate_alleles)', '6')) -maxNumHaplotypesInPopulation $(WDLCommandPart('NonNull(inputs.maxNumHaplotypesInPopulation)', '128')) -maxReadsInRegionPerSample $(WDLCommandPart('NonNull(inputs.maxReadsInRegionPerSample)', '10000')) -mbq $(WDLCommandPart('NonNull(inputs.min_base_quality_score)', '10')) -minDanglingBranchLength $(WDLCommandPart('NonNull(inputs.minDanglingBranchLength)', '4')) -minPruning $(WDLCommandPart('NonNull(inputs.minPruning)', '2')) -minReadsPerAlignStart $(WDLCommandPart('NonNull(inputs.minReadsPerAlignmentStart)', '10')) -numPruningSamples $(WDLCommandPart('NonNull(inputs.numPruningSamples)', '1')) -o $(WDLCommandPart('NonNull(inputs.out)', 'stdout')) -out_mode $(WDLCommandPart('NonNull(inputs.output_mode)', 'EMIT_VARIANTS_ONLY')) -pcrModel $(WDLCommandPart('NonNull(inputs.pcr_indel_model)', 'CONSERVATIVE')) -globalMAPQ $(WDLCommandPart('NonNull(inputs.phredScaledGlobalReadMismappingRate)', '45')) $(WDLCommandPart('\"-sn \" + NonNull(inputs.sample_name)', '')) -ploidy $(WDLCommandPart('NonNull(inputs.sample_ploidy)', '2')) -stand_call_conf $(WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_calling)', '30.0')) -stand_emit_conf $(WDLCommandPart('NonNull(inputs.standard_min_confidence_threshold_for_emitting)', '30.0')) $(defHandler('-allelesTrigger', WDLCommandPart('NonNull(inputs.useAllelesTrigger)', 'false'))) $(defHandler('-useFilteredReadsForAnnotations', WDLCommandPart('NonNull(inputs.useFilteredReadsForAnnotations)', 'false'))) $(WDLCommandPart('NonNull(inputs.userString)', ''))"
        }
    ], 
    "id": "HaplotypeCaller"
}