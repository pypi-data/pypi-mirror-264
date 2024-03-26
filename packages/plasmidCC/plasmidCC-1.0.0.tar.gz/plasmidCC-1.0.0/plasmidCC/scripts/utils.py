import os
import sys
import argparse
from rich import print as rprint


def quit_tool(exitcode):
    if exitcode != 0:
        rprint('\n', end='')
        rprint("[bold red]This run of plasmidCC has ended unexpectedly. Pease check above for any error messages")
        sys.exit(1)
    else:
        rprint("[bold green]plasmidCC has succesfully completed running, thanks for using plasmidCC!")
        sys.exit(0)


def is_valid_dir(arg):
    if not os.path.isdir(arg):
        rprint(f"[bold red]'{arg}' is not an existing directory, and I am afraid to create it")
        raise argparse.ArgumentTypeError()
    return arg


def is_valid_file(arg, extensions=['fasta', 'gfa']):
    if not os.path.isfile(arg):
        rprint(f"[bold red]'{arg}' is not an existing file. Please make sure the file exists")
        raise argparse.ArgumentTypeError()
    _, file_extension = os.path.splitext(arg)
    if not file_extension[1:].lower() in extensions:
        rprint(f"[bold red]'{arg}' is not a file of type {' or '.join(extensions)}")
        raise argparse.ArgumentTypeError()
    return arg


def verify_user_db(arg):
    filename = os.path.basename(arg)
    basename, file_extension = os.path.splitext(filename)
    if file_extension != '':
        all_extensions = '.'.join(filename.split(os.extsep)[1:])
        rprint(f"[bold red]Input name '{filename}' contains a file extension")
        rprint(f"[bold red]Please remove any file extensions from your input name ('.{all_extensions}')")
        raise argparse.ArgumentTypeError()
    elif not os.path.isfile(f"{arg}.3.cf"):
        dirname = os.path.dirname(arg)
        rprint(f"[bold red]Database '{basename}.3.cf' does not exist in path '{dirname}'")
        rprint("[bold red]Please make sure everything is spelled correctly")
        raise argparse.ArgumentTypeError()
    else:
        return arg


# Database names for embedded species
dbnames = {"General":"general_plasmid_db",
           "Escherichia_coli":"chromosome_plasmid_db",
           "Enterococcus_faecium":"E_faecium_c_plasmid_db",
           "Enterococcus_faecalis":"E_faecalis_c_plasmid_db",
           "Salmonella_enterica":"S_enterica_plasmid_db",
           "Staphylococcus_aureus":"S_aureus_plasmid_db",
           "Acinetobacter_baumannii":"A_baumannii_plasmid_db",
           "Klebsiella_pneumoniae":"K_pneumoniae_plasmid_db"}
speciesopts = dbnames.keys()
def check_species(arg):
    if arg not in speciesopts:
        rprint(f"[bold red]'{arg}' is not a recognised species")
        rprint("[bold red]Use plasmidCC with the --speciesopts flag for a list of all supported species")
        raise argparse.ArgumentTypeError()
    return arg


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_empty_dir(dir_path):
    if os.path.exists(dir_path):
        if not any(os.listdir(dir_path)):
            os.rmdir(dir_path)


def cleanup_intermediary_files(outdir, inname):
    delete_file(os.path.join(outdir, f"{inname}_summary.txt"))
    delete_file(os.path.join(outdir, f"{inname}_filtered.fasta"))
    delete_file(os.path.join(outdir, f"{inname}_centrifuge_results.txt"))
    delete_file(os.path.join(outdir, "logs", "centrifuge_log.txt"))
    delete_empty_dir(os.path.join(outdir, "logs"))


def cleanup_all_files(outdir, inname):
    cleanup_intermediary_files(outdir, inname)
    delete_file(os.path.join(outdir, f"{inname}_plasmids.fasta"))
    delete_file(os.path.join(outdir, f"{inname}_centrifuge_classified.txt"))
    delete_file(os.path.join(outdir, f"{inname}_gplas.tab"))