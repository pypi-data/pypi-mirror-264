import os
import pandas as pd
import numpy as np


def write_fasta(processed_df, sequence_map, outdir, inname):
    """
    Writes fasta file with only the plasmid predicted contigs.
    If none are available, sends message.
    """
    output_file = os.path.join(outdir, f"{inname}_plasmids.fasta")
    sequence_names = {key.lstrip('>'): value for key, value in sequence_map.items()}
    plasmids = processed_df[processed_df['final_classification'] == 'plasmid']['readID']

    if len(plasmids) == 0:
        return False
    else:
        with open(output_file, 'w') as outfile:
            for header in plasmids:
                outfile.write(f">{header}\n{sequence_names[header]}\n")
    return True


def remove_spaces(seq_id):
    """
    If spaces, remove them
    """
    return seq_id.split(' ')[0]


def extract_gplas(wide_counts, sequence_map, outdir, inname):
    """
    Create gplas output
    """
    wide_counts = wide_counts.copy()
    output_file = os.path.join(outdir, f"{inname}_gplas.tab")
    sequence_lengths = {key.lstrip('>'): len(value) for key, value in sequence_map.items()}

    # Replace 'unclassified' with 'plasmid' in Final_classification
    wide_counts['final_classification'] = wide_counts['final_classification'].replace('unclassified', 'plasmid')

    # Replace predictions with capital letters
    wide_counts['final_classification'] = wide_counts['final_classification'].str.replace('plasmid', 'Plasmid')
    wide_counts['final_classification'] = wide_counts['final_classification'].str.replace('chromosome', 'Chromosome')

    # Modify data frame to fit gplas requirements
    wide_counts = wide_counts.loc[:, ['chromosome_fraction', 'plasmid_fraction', 'final_classification', 'readID']]

    wide_counts.columns = ['Prob_Chromosome', 'Prob_Plasmid', 'Prediction', 'Contig_name']
    wide_counts.loc[:, 'Contig_length'] = wide_counts.loc[:, 'Contig_name'].map(sequence_lengths)

    without_spaces = wide_counts['Contig_name'].apply(remove_spaces)
    wide_counts.loc[:, 'Contig_name'] = without_spaces

    wide_counts.to_csv(output_file, sep='\t', index=False)


def process(indir, inname, outdir, plasmid_cutoff, chromosome_cutoff):
    """
    Process Centrifuge output file.
    Raw Centrifuge output is read, names are assigned to the taxa IDs
    Counts occurrences of classifications per sequence
    Calculates total matches, fraction of chromosomes and fraction of plasmids
    Votes for classification based on >70% plasmid hits
    """
    input_path = os.path.join(indir, f"{inname}_centrifuge_results.txt")
    output_path = os.path.join(outdir, f"{inname}_centrifuge_classified.txt")
    centrifuge_raw = pd.read_csv(input_path, sep='\t', header=0)

    replace_dict = {2:'chromosome', 3:'plasmid', 0:'unclassified'}
    centrifuge_raw['taxID'] = centrifuge_raw['taxID'].apply(lambda x: 0 if x > 3 else x)
    centrifuge_raw['taxID'] = centrifuge_raw['taxID'].replace(replace_dict)

    cf_count = centrifuge_raw.groupby(['readID', 'taxID'])['taxID'].count().reset_index(name='count')
    cf_count_wide = cf_count.pivot(index='readID', columns='taxID', values='count').fillna(0).reset_index()

    for col in ['chromosome', 'plasmid', 'unclassified']:
        if col not in cf_count_wide.columns:
            cf_count_wide[col] = 0

    cf_count_wide['total_matches'] = cf_count_wide['chromosome'] + cf_count_wide['plasmid'] + cf_count_wide['unclassified']
    cf_count_wide['chromosome_fraction'] = round(cf_count_wide['chromosome'] / cf_count_wide['total_matches'], 2)
    cf_count_wide['plasmid_fraction'] = round(cf_count_wide['plasmid'] / cf_count_wide['total_matches'], 2)

    # If there are unclassfied entries, they will always be called unclassified
    cf_count_wide['chromosome_fraction'] = cf_count_wide.apply(lambda row: 0.5 if row['unclassified'] != 0 else row['chromosome_fraction'], axis=1)
    cf_count_wide['plasmid_fraction'] = cf_count_wide.apply(lambda row: 0.5 if row['unclassified'] != 0 else row['plasmid_fraction'], axis=1)

    cf_count_wide['final_classification'] = np.where(cf_count_wide['plasmid_fraction'] >= plasmid_cutoff, 'plasmid',
                                                     np.where(cf_count_wide['plasmid_fraction'] < chromosome_cutoff, 'chromosome', 'unclassified'))
    cf_count_wide.to_csv(output_path, sep='\t', index=False)
    return cf_count_wide
