import os
import sys
import argparse
from rich import print as rprint
import plasmidCC.scripts.utils as utils
import plasmidCC.scripts.download_centrifuge_db as download_centrifuge_db
import plasmidCC.scripts.extract_nodes as extract_nodes
import plasmidCC.scripts.run_centrifuge as run_centrifuge
import plasmidCC.scripts.process_centrifuge as process_centrifuge
from plasmidCC.version import version as VERSION
#VERSION = "1.0.0"
# Directories
# Current installed directory
pkgdir = os.path.dirname(__file__)
default_db_dir = f"{pkgdir}/databases"


class PriorityPrinting(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if option_string == '-h' or option_string == '--help':
            parser.print_help()
        elif option_string == '-v' or option_string == '--version':
            print(f"plasmidCC version {VERSION}")
        elif option_string == '--speciesopts':
            for species in utils.speciesopts:
                if species == 'General':
                    print(species, "(warning: general database requires >47GB of availabe RAM)")
                else:
                    print(species)
        parser.exit()


def main(args=sys.argv[1:]):
    """
    Main function creates an argument parser for CLI running. It checks input files and runs the plasmidCC main functionalities.
    """
    parser = argparse.ArgumentParser(description="PlasmidCC: A Centrifuge based plasmid prediction tool", add_help=False)
    parser.register('action', 'printing', PriorityPrinting)

    # argument group for general parameters
    inputgroup = parser.add_argument_group('General')
    inputgroup.add_argument('-i', dest='input', type=utils.is_valid_file, required=True, help="input file (.fasta or .gfa)")
    inputgroup.add_argument('-o', dest='output', type=utils.is_valid_dir, default=".", help="Output directory")
    inputgroup.add_argument('-n', dest='name', type=str, help="Name prefix for output files (default: input file name)")

    # User can either select embedded species or own supplied db
    databasegroup = inputgroup.add_mutually_exclusive_group(required=True)
    databasegroup.add_argument('-s', dest='species', type=utils.check_species, help="Select an embedded species database. Use --speciesopts for a list of all supported species")
    databasegroup.add_argument('-p', dest='custom_db_path', type=utils.verify_user_db, help="Path to a custom Centrifuge database (name without file extensions)")

    # Customizable parameters in argument group
    paramgroup = parser.add_argument_group('Parameters')
    paramgroup.add_argument('-l', dest='length', type=int, default=1000, help="Minimum sequence length filter (default: %(default)s)")
    paramgroup.add_argument('-t', dest='threads', type=int, default=8, help="Number of alignment threads to launch (default: %(default)s)")
    paramgroup.add_argument('-P', dest='plasmid_cutoff', type=float, default=0.7, help="Threshold of plasmid fraction to predict contig as plasmid (default: %(default)s)")
    paramgroup.add_argument('-C', dest='chromosome_cutoff', type=float, default=0.3, help="Threshold of plasmid fraction to predict contig as chromosome (default: %(default)s)")

    # Utility options
    othergroup = parser.add_argument_group('Other')
    othergroup.add_argument('-D', '--download', action='store_true', help="Download embedded database if not yet downloaded")
    othergroup.add_argument('-g', '--gplas', action='store_true', help="Write an extra output file that is compatible for use with gplas")
    othergroup.add_argument('-f', '--force', action='store_true', help="Overwrite existing output if the same name is already used")
    othergroup.add_argument('-k', '--keep', action='store_true', help="Keep intermediary files")

    # plasmidCC version and usage info
    infogroup = parser.add_argument_group('Info')
    infogroup.add_argument('--speciesopts', action='printing', nargs=0, help="Prints a list of all supported species for the -s flag")
    infogroup.add_argument('-v', '--version', action='printing', nargs=0, help="Prints plasmidCC version")
    infogroup.add_argument('-h', '--help', action='printing', nargs=0, help="Prints this message")
    args = parser.parse_args()

    # Establish absolute path to database
    if args.species:
        cent_db_name = utils.dbnames[args.species]
        cent_db_dir = os.path.abspath(default_db_dir)
    elif args.custom_db_path:
        cent_db_name = os.path.basename(args.custom_db_path)
        cent_db_dir = os.path.abspath(os.path.dirname(args.custom_db_path))

    cent_db_path = os.path.abspath(os.path.join(cent_db_dir, cent_db_name))

    # Checks if embedded database already exists or if the user wants to explicitly download it from our Zenodo
    if args.species and not os.path.isfile(f"{cent_db_dir}/{cent_db_name}.3.cf"):
        rprint(f"[bold yellow]Database [bold white]'{cent_db_name}' [bold yellow]is not downloaded yet")
        if not args.download:
            rprint("[bold yellow]Use the -D/--download flag if you wish to download this database")
            utils.quit_tool(-1)
        else:
            rprint("[bold yellow]We will be downloading this database now")
            download_centrifuge_db.download(cent_db_name, cent_db_dir)

    rprint(f"[bold green]PlasmidCC will run using the database [bold white]'{cent_db_name}' [bold green]in [bold white]'{cent_db_dir}'")

    infilename = os.path.basename(args.input)  # filename with extension

    # Check if the user specified a run name or to use file name data
    if args.name:
        inname = args.name
        _, informat = os.path.splitext(infilename)
    else:
        inname, informat = os.path.splitext(infilename)  # filename and extension

    outdir = os.path.abspath(os.path.join(f"{args.output}", f"{inname}"))
    rprint(f"[bold green]Output will be saved in [bold white]'{outdir}'")
    fastaname = os.path.join(outdir, f"{inname}_filtered.fasta")
    
    # Check if plasmidCC output already exists
    if os.path.isfile(f"{outdir}/{inname}_centrifuge_classified.txt") or os.path.isfile(f"{outdir}/{inname}_gplas.tab"):
        rprint(f"[bold yellow]plasmidCC output is already present for '{inname}'")
        if args.force:
            rprint("[bold yellow]! Previous output will be overwritten !")
            utils.cleanup_all_files(outdir, inname)
        else:
            rprint("[bold yellow]Please check if all your input arguments are correct")
            rprint("[bold yellow]Use the -f/--force flag to ignore this warning and overwrite existing output")
            utils.quit_tool(-1)

    # Make output/logs directory
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(f"{outdir}/logs", exist_ok=True)

    # Extract contigs from input file
    sequence_map = extract_nodes.extract_nodes(args.input, fastaname, informat, args.length)

    # Run Centrifuge
    rprint("[bold yellow]Running Centrifuge...", end='\r')
    run_centrifuge.run(fastaname, outdir, cent_db_path, args.threads, inname, pkgdir)
    rprint("[bold green]Finished running Centrifuge")

    # Transform Centrifuge output
    rprint("[bold yellow]Processing Centrifuge output...", end='\r')
    wide_counts = process_centrifuge.process(outdir, inname, outdir, args.plasmid_cutoff, args.chromosome_cutoff)

    # Gplas parsing
    if args.gplas:
        process_centrifuge.extract_gplas(wide_counts, sequence_map, outdir, inname)

    rprint("[bold green]Finished processing Centrifuge output")
    
    # Write plasmid contigs
    rprint("[bold yellow]Writing plasmid sequences to fasta...", end='\r')
    plasmids = process_centrifuge.write_fasta(wide_counts, sequence_map, outdir, inname)
    if plasmids:
        rprint("[bold green]Finished writing plasmid sequences to fasta")
    else:
        rprint("[bold yellow]No plasmids were predicted in your sample")
    
    # If the -k flag was not selected, delete intermediary files
    if not args.keep:
        utils.cleanup_intermediary_files(outdir, inname)

    utils.quit_tool(0)

if __name__ == '__main__':
    main()
