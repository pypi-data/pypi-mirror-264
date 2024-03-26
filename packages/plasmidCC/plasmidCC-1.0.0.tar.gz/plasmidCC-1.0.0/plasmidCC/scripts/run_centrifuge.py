import subprocess
import shutil
import os
from rich import print as rprint
from utils import quit_tool


def run(fastaname, outdir, cent_db_path, threads, inname, pkgdir):
    summary = os.path.join(outdir, f"{inname}_summary.txt")
    results = os.path.join(outdir, f"{inname}_centrifuge_results.txt")
    logs = os.path.join(outdir, "logs", "centrifuge_log.txt")
    if shutil.which('centrifuge'):
        with open(logs, 'w') as log:
            cmd = f"centrifuge -f --threads {threads} -x {cent_db_path} -U {fastaname} -k 1000 --report-file {summary} -S {results}"
            try:
                subprocess.run(cmd, shell=True, check=True, stdout=log, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                rprint("[bold red]Centrifuge has run into an error!")
                rprint(f"[bold red]Check '{logs}' for more information")
                quit_tool(e.returncode)
    else:
        rprint("[bold red]Centrifuge is not installed, please verify your installation.")
        quit_tool(-1)
