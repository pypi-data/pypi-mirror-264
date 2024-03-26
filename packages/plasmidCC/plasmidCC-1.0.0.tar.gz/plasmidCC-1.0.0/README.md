

# PlasmidCC

PlasmidCC is a plasmid classification tool that uses [Centrifuge](https://ccb.jhu.edu/software/centrifuge) to predict the origin of contigs (plasmid or chromosome).

PlasmidCC is a generalization of [PlasmidEC](https://gitlab.com/mmb-umcu/plasmidEC), which uses multiple classification tools to classify plasmids in _E. coli_ isolates.
## Table of contents
* [Installation](#installation)
* [Usage](#usage)
  * [Input](#input)
  * [Quick usage](#quick-usage)
  * [Other species](#other-species)
  * [All options](#all-options)   
* [Output files](#output-files)
  * [Compatibility with gplas](#compatibility-with-gplas)
  * [Intermediary files](#intermediary-files)
* [Contributions](#contributions)
* [Citation](#citation)


## Installation
An installation of [Centrifuge](https://ccb.jhu.edu/software/centrifuge) is required to run plasmidCC

We recommend using a conda environment with the [centrifuge-core](https://bioconda.github.io/recipes/centrifuge-core/README.html) package installed:
```
conda create --name plasmidCC -c conda-forge -c bioconda centrifuge-core=1.0.4.1 pip
conda activate plasmidCC
``` 

Install plasmidCC using pip:
```
pip install plasmidCC
```

Verify installation:
```
plasmidCC --help
```

## Usage
### Test run example
```
plasmidCC -i test/test_ecoli.gfa -o test -n testEcoli -s Escherichia_coli -D
```
This will use the 'test_ecoli.gfa' file as input (**-i**), and store output in the 'test' directory (**-o**) under a new subdirectory named 'testEcoli' (**-n**). plasmidCC will look for the embedded database of E. coli (**-s**) and when not found, it will try to download this database (**-D**). 

### Input
As input, plasmidCC takes assembled contigs in **.fasta** format **or** an assembly graph in **.gfa** format. Such files can be obtained with [Unicycler](https://github.com/rrwick/Unicycler) or [SPAdes genome assembler](https://github.com/ablab/spades).

### Quick usage
Out of the box, plasmidCC can be used to predict plasmid contigs of certain embedded species. Use the **-\-speciesopts** flag to see a list of supported species:
```
plasmidCC --speciesopts
```
```
General (warning: general database requires >47GB of availabe RAM)
Escherichia_coli
Enterococcus_faecium
Enterococcus_faecalis
Salmonella_enterica
Staphylococcus_aureus
Acinetobacter_baumannii
Klebsiella_pneumoniae
```

You can specify which species database to use with the **-s** flag. For example:
```
plasmidCC -i test/K_pneumoniae_test.fasta -s Klebsiella_pneumoniae
```

### Other species
It is possible to use plasmidCC for other species. However, a custom Centrifuge database will have to be constructed for the desired species. Instructions on how to do this can be found [here](https://ccb.jhu.edu/software/centrifuge/manual.shtml#custom-database).
Once constructed, the location and name of your custom database can be supplied to plasmidCC by using the **-p** flag:
```
plasmidCC -i test/P_aeruginosa_test.fasta -p databases/my_custom_db
```

### All options
```
plasmidCC --help
```
```
usage: plasmidCC -i INPUT [-o OUTPUT] [-n NAME] (-s SPECIES | -p CUSTOM_DB_PATH) [-l LENGTH]
                 [-t THREADS] [-P PLASMID_CUTOFF] [-C CHROMOSOME_CUTOFF] [-D] [-g] [-f] [-k]
                 [--speciesopts] [-v] [-h]

PlasmidCC: a Centrifuge based plasmid prediction tool

General:
  -i INPUT              input file (.fasta or .gfa)
  -o OUTPUT             Output directory
  -n NAME               Name prefix for output files (default: input file name)
  -s SPECIES            Select an embedded species database. Use --speciesopts for a list of all
                        supported species
  -p CUSTOM_DB_PATH     Path to a custom Centrifuge database (name without file extensions)

Parameters:
  -l LENGTH             Minimum sequence length filter (default: 1000)
  -t THREADS            Number of alignment threads to launch (default: 8)
  -P PLASMID_CUTOFF     Threshold of plasmid fraction to predict contig as plasmid (default: 0.7)
  -C CHROMOSOME_CUTOFF  Threshold of plasmid fraction to predict contig as chromosome (default: 0.3)

Other:
  -D, --download        Download embedded database if not yet downloaded
  -g, --gplas           Write an extra output file that is compatible for use with gplas
  -f, --force           Overwrite existing output if the same name is already used
  -k, --keep            Keep intermediary files

Info:
  --speciesopts         Prints a list of all supported species for the -s flag
  -v, --version         Prints plasmidCC version
  -h, --help            Prints this message
```

## Output Files

#### plasmids.fasta
Sequences of all contigs predicted to originate from plasmids in FASTA format.
```
grep '>' test/testEcoli/testEcoli_plasmids.fasta
```
```
>S20_LN:i:91233_dp:f:0.5815421095375989
>S32_LN:i:42460_dp:f:0.6016122804021161
>S44_LN:i:21171_dp:f:0.5924640018897323
>S47_LN:i:17888_dp:f:0.5893320957724726
>S50_LN:i:11225_dp:f:0.6758514700227541
>S56_LN:i:6837_dp:f:0.5759570101860518
>S59_LN:i:5519_dp:f:0.5544497698217399
>S67_LN:i:2826_dp:f:0.6746421335091037
>S76_LN:i:1486_dp:f:1.3509551203209675
```

#### centrifuge_classified.txt
Table containing the predictions made by Centrifuge, the total nr. of matches, and the final classification for each contig.
```
head -n 5 test/testEcoli/testEcoli_centrifuge_classified.txt
```
| readID | chromosome | plasmid | unclassified | total_matches | chromosome_fraction | plasmid_fraction | final_classification |
| ------ | ---------- | ------- | ------------ | ------------- | ------------------- | ---------------- | -------------------- | 
| S80_LN:i:1427_dp:f:0.9617101819819399 | 2.0 | 0.0 | 0 | 2.0 | 1.0 | 0.0 | chromosome |
| S81_LN:i:1343_dp:f:4.494970368199747 | 117.0 | 40.0 | 0 | 157.0 | 0.75 | 0.25 | chromosome |
| S82_LN:i:1253_dp:f:1.182459332915489 | 1.0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | chromosome |
| S83_LN:i:1242_dp:f:0.9224653122847608 | 1.0 | 0.0 | 0 | 1.0 | 1.0 | 0.0 | chromosome |
| S84_LN:i:1063_dp:f:3.2697611578099566 | 118.0 | 33.0 | 0 | 151.0 |  0.78 | 0.22 | chromosome |

### Compatibility with gplas
[gplas](https://gitlab.com/mmb-umcu/gplas) is a tool that accurately bins predicted plasmid contigs into individual plasmids.

By using the **-g** flag, plasmidCC provides an extra output file that can be directly used as input for gplas. See an example below:
```
plasmidCC -i test/test_ecoli.gfa -o test -n testEcoli -s Escherichia_coli -g
```
```
head -n 10 test/testEcoli/testEcoli_gplas.tab
```
| Prob_Chromosome | Prob_Plasmid | Prediction | Contig_name | Contig_length |
| --------------- | ------------ | ---------- | ----------- | ------------- |
| 1.0 | 0.0 | Chromosome | S10_LN:i:198295_dp:f:0.8919341045340952 | 198295 |
| 1.0 | 0.0 | Chromosome | S11_LN:i:173581_dp:f:0.8682632509656248 | 173581 |
| 1.0 | 0.0 | Chromosome | S12_LN:i:169985_dp:f:1.0893451820087325 | 169985 |
| 1.0 | 0.0 | Chromosome | S13_LN:i:169238_dp:f:1.1143772255735436 | 169238 |
| 1.0 | 0.0 | Chromosome | S14_LN:i:135734_dp:f:0.8900147755192753 | 135734 |
| 1.0 | 0.0 | Chromosome | S15_LN:i:114916_dp:f:0.8135597349289454 | 114916 |
| 1.0 | 0.0 | Chromosome | S16_LN:i:112152_dp:f:0.9565731810452665 | 112152 |
| 1.0 | 0.0 | Chromosome | S17_LN:i:107357_dp:f:1.0935311833495955 | 107357 |
| 1.0 | 0.0 | Chromosome | S18_LN:i:105440_dp:f:0.9191174721979478 | 105440 |

### Intermediary files
By default, intermediary files will get deleted at the end of a run. Use the **-k** flag to keep intermediary files.

#### centrifuge_results.txt
Raw Centrifuge classification output that is used by plasmidCC to produce the 'centrifuge_classified.txt' output.

#### summary.txt
Centrifuge report file summarizing details per classification group.

#### filtered.fasta
Input sequences (**-i**) filtered for minimum sequence length (**-l**). This file is used when running Centrifuge.


## Contributions

PlasmidCC has been developed with contributions from Lisa Vader, Malbert Rogers, Julian Paganini, Jesse Kerkvliet, Anita Schürch and Oscar Jordan.

## Citation

If you use plasmidCC, please cite:

(Citation follows)
