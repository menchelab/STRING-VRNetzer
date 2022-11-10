import gzip
import os
import sys
from ast import alias

import requests


def download(tax_id, organism):
    """Used to download necessary files from STRING database to create full genome networks."""
    url = "https://stringdb-static.org/download/"
    links = "protein.links.detailed.v11.5/"
    info = "protein.info.v11.5/"
    ali = "protein.aliases.v11.5/"
    organism_links = f"{tax_id}.protein.links.detailed.v11.5.txt.gz"
    organism_info = f"{tax_id}.protein.info.v11.5.txt.gz"
    organism_aliases = f"{tax_id}.protein.aliases.v11.5.txt.gz"
    directory = f"./STRING/{organism}"
    os.makedirs(directory, exist_ok=True)
    for data, file in zip(
        [links, info, ali],
        [organism_links, organism_info, organism_aliases],
    ):
        if not os.path.exists(os.path.join(directory, file.strip(".gz"))):
            print(url + data + file)
            r = requests.get(url + data + file)
            content = gzip.decompress(r.content)
            with open(os.path.join(directory, file.strip(".gz")), "wb+") as f:
                f.write(content)


if __name__ == "__main__":
    organisms = {
        "human": 9606,
        "mouse": 10090,
        "rat": 10116,
        "zebrafish": 7955,
        "fruitfly": 7227,
        "worm": 6239,
        "yeast": 4932,
        "ecoli": 362663,
        "arabidopsis": 3702,
    }
    for organism, tax_id in organisms.items():
        download(tax_id, organism)
