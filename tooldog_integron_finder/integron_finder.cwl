#!/usr/bin/env cwl-runner

$namespaces: {edam: https://edamontology.org/, s: http://schema.org/}
class: CommandLineTool
cwlVersion: v1.0
doc: |+
  A tool to detect Integron in DNA sequences

  External links:
  Tool homepage: https://github.com/gem-pasteur/Integron_Finder
  bio.tools entry: integron_finder

inputs:
  attc_model:
    default: attc_4.cm
    doc: path or file to the attc model (Covariance Matrix)
    inputBinding: {prefix: --attc_model}
    type: ['null', string]
  cmsearch:
    doc: Complete path to cmsearch if not in PATH. eg - /usr/local/bin/cmsearch
    inputBinding: {prefix: --cmsearch}
    type: ['null', string]
  cpu:
    default: 1
    doc: Number of CPUs used by INFERNAL and HMMER
    inputBinding: {prefix: --cpu}
    type: ['null', string]
  distance_thresh:
    default: 4000
    doc: Two elements are aggregated if they are distant of DISTANCE_THRESH [4kb]
      or less
    inputBinding: {prefix: --distance_thresh}
    type: ['null', int]
  eagle_eyes:
    doc: Synonym of --local_max. Like a soaring eagle in the sky, catching rabbits(or
      attC sites) by surprise.
    inputBinding: {prefix: --eagle_eyes}
    type: ['null', boolean]
  evalue_attc:
    default: 1.0
    doc: set evalue threshold to filter out hits above it (default - 1)
    inputBinding: {prefix: --evalue_attc}
    type: ['null', float]
  func_annot:
    doc: Functional annotation of CDS associated with integrons HMM files are needed
      in Func_annot folder.
    inputBinding: {prefix: --func_annot}
    type: ['null', boolean]
  gembase:
    doc: Use gembase formatted protein file instead of Prodigal. Folder structure
      must be preserved
    inputBinding: {prefix: --gembase}
    type: ['null', boolean]
  hmmsearch:
    doc: Complete path to hmmsearch if not in PATH. eg - /usr/local/bin/hmmsearch
    inputBinding: {prefix: --hmmsearch}
    type: ['null', string]
  keep_palindromes:
    doc: for a given hit, if the palindromic version is found, don't remove the one
      with highest evalue
    inputBinding: {prefix: --keep_palindromes}
    type: ['null', boolean]
  linear:
    doc: Consider replicon as linear. If replicon smaller than 20kb, it will be considered
      as linear
    inputBinding: {prefix: --linear}
    type: ['null', boolean]
  local_max:
    doc: Allows thorough local detection (slower but more sensitive and do not increase
      false positive rate).
    inputBinding: {prefix: --local_max}
    type: ['null', boolean]
  max_attc_size:
    default: 200
    doc: set maximum value fot the attC size (default - 200bp)
    inputBinding: {prefix: --max_attc_size}
    type: ['null', int]
  min_attc_size:
    default: 40
    doc: set minimum value fot the attC size (default - 40bp)
    inputBinding: {prefix: --min_attc_size}
    type: ['null', int]
  no_proteins:
    doc: Don't annotate CDS and don't find integrase, just look for attC sites.
    inputBinding: {prefix: --no_proteins}
    type: ['null', boolean]
  outdir:
    default: .
    doc: Set the output directory (default - current)
    inputBinding: {prefix: --outdir}
    type: ['null', string]
  path_func_annot:
    doc: Path to file containing all hmm bank paths (one per line)
    inputBinding: {prefix: --path_func_annot}
    type: ['null', string]
  prodigal:
    doc: Complete path to prodigal if not in PATH. eg - /usr/local/bin/prodigal
    inputBinding: {prefix: --prodigal}
    type: ['null', string]
  replicon:
    doc: Path to the replicon file (in fasta format), eg - path/to/file.fst or file.fst
    inputBinding: {position: 1}
    type: string
  union_integrases:
    doc: Instead of taking intersection of hits from Phage_int profile (Tyr recombinases)
      and integron_integrase profile, use the union of the hits
    inputBinding: {prefix: --union_integrases}
    type: ['null', boolean]
s:about: A tool to detect Integron in DNA sequences
s:keywords: [edam:topic_0085, edam:topic_0798, edam:topic_3047, edam:topic_0091, edam:topic_0080]
s:name: Integron Finder
s:programmingLanguage: [Python]
s:publication:
- {id: http://dx.doi.org/10.1093/nar/gkw319}
s:url: https://github.com/gem-pasteur/Integron_Finder

None
