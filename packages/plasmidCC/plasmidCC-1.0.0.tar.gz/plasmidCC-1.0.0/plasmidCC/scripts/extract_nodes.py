from Bio.SeqIO.FastaIO import SimpleFastaParser


def extract_gfa(filename):
    """
    Opens gfa file, checks for segments (S) and parses to fasta.
    Returns dictionary of sequence headers and their sequence
    """
    sequences = {}
    with open(filename, 'r') as gfa_file:
        for line in gfa_file:
            info = line.strip().split('\t')
            if info[0] == 'S':
                if 'LN' in str(info[3]):  # Unicycler assembly
                    header = f">{info[0]}{info[1]}_{info[3]}_{info[4]}"
                elif 'KC' in str(info[3]):  # Spades assembly
                    header = f">{info[0]}{info[1]}_{info[3]}"
                else:  # Empty sequence field (0 length), or other error in gfa format
                    continue  # Skip node and continue to the next
                sequence = info[2]
                sequences[header] = str(sequence)
    return sequences


def extract_fasta(filename):
    """
    Creates dictionary with fasta headers and sequences
    """
    sequences = {}
    with open(filename, 'r') as fasta_file:
        for header, sequence in SimpleFastaParser(fasta_file):
            sequences[f">{header}"] = str(sequence)
    return sequences


def remove_short_contigs(sequences, fastaname, minlen):
    """
    Takes dictionary with fasta headers and sequences. Filters for sequence length
    and writes to fasta output
    """
    with open(fastaname, 'w') as fasta_file:
        for s in sequences.keys():
            if len(sequences[s]) > minlen:
                fasta_file.write(f"{s}\n{sequences[s]}\n")


def extract_nodes(filename, fastaname, informat, minlen):
    """
    Main function checks if the format is a legitimate sequence format.
    Calls the extraction functions and the writing/filtering function
    """
    informat = informat.strip('.')
    if informat == 'gfa':
        sequences = extract_gfa(filename)
    elif informat == 'fasta':
        sequences = extract_fasta(filename)
    remove_short_contigs(sequences, fastaname, minlen)
    return sequences
