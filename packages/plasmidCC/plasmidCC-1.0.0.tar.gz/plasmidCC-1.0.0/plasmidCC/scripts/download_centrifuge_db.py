import os
import urllib3
import tarfile
from rich import print as rprint
from utils import quit_tool

# Dictionary with databases
database_urls = {
    "chromosome_plasmid_db":"https://zenodo.org/record/1311641/files/chromosome_plasmid_db.tar.gz",
    "E_faecium_c_plasmid_db":"https://zenodo.org/records/10472051/files/E_faecium_centrifuge_db.tar.gz",
    "E_faecalis_c_plasmid_db":"https://zenodo.org/records/10471306/files/E_faecalis_centrifuge_db.tar.gz",
    "A_baumannii_plasmid_db":"https://zenodo.org/record/7326823/files/A_baumannii_plasmid_db.tar.gz",
    "S_aureus_plasmid_db":"https://zenodo.org/record/7133406/files/S_aureus_plasmid_db.tar.gz",
    "S_enterica_plasmid_db":"https://zenodo.org/record/7133407/files/S_enterica_plasmid_db.tar.gz",
    "K_pneumoniae_plasmid_db":"https://zenodo.org/record/7194565/files/K_pneumoniae_plasmid_db.tar.gz",
    "general_plasmid_db":"https://zenodo.org/record/7431957/files/general_plasmid_db.tar.gz"
}


def download(cent_db_name, cent_db_dir):
    rprint("[bold yellow]Preparing download...", end='\r')
    database_url = database_urls[cent_db_name]
    tarpath = os.path.join(cent_db_dir, f"{cent_db_name}.tar.gz")
    http = urllib3.PoolManager()

    with http.request('GET', database_url, preload_content=False) as response:
        if response.status == 200:
            rprint(f"[bold yellow]Downloading database [bold white]'{cent_db_name}' [bold yellow]into [bold white]'{cent_db_dir}'")
            rprint(f"[bold yellow]This might take a while... (download size: {round(int(response.headers['content-length'])/float(1<<20), 2)} MB)")
            with open(tarpath, 'wb') as out_file:
                for chunk in response.stream(8192):
                    out_file.write(chunk)
            rprint("[bold green]Finished downloading")
        else:
            rprint(f"[bold red]Downloading failed with error code {response.status}")
            quit_tool(-1)
    rprint("[bold yellow]Extracting ZIP file...", end='\r')
    with tarfile.open(tarpath, 'r:gz') as tar:
        tar.extractall(path=cent_db_dir)
    rprint("[bold green]Finished ZIP extraction")
    os.remove(tarpath)
