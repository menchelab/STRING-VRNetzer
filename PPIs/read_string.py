import glob
import json
import os

import pandas

import settings as st
import util
from settings import LinkTags as LiT
from settings import NodeTags as NT
from settings import VRNetzElements as VRNE


def write_VRNetz(organism, networks_directory, last=None):
    link_file, alias_file, description_file = "", "", ""
    directory = os.path.join(
        networks_directory, st.Organisms.get_directory_name(organism)
    )
    for file in glob.glob(os.path.join(directory, "*")):
        if file.endswith("protein.links.detailed.v11.5.txt"):
            link_file = file
        elif file.endswith(".protein.aliases.v11.5.txt"):
            alias_file = file
        elif file.endswith(".protein.info.v11.5.txt"):
            description_file = file
    species = st.Organisms.get_scientific_name(organism)
    network_table = pandas.read_table(link_file, header=0, sep=" ")
    alias_table = pandas.read_table(
        alias_file,
        header=0,
        sep="\t",
        index_col=0,
    )
    description_table = pandas.read_table(
        description_file, header=0, sep="\t", index_col=0
    )
    network = {
        VRNE.nodes: [],
        VRNE.links: [],
        VRNE.node_layouts: [],
        VRNE.link_layouts: [ev for ev in st.Evidences.get_default_scheme().keys()],
    }
    nodes_in = {}
    next_id = 0
    ev_columns = [
        "neighborhood",
        "fusion",
        "cooccurence",
        "coexpression",
        "experimental",
        "database",
        "textmining",
    ]
    if last is None:
        last = len(network_table)

    for idx in range(last):
        row = network_table.iloc[idx]
        link = {}
        s_node = {}
        e_node = {}
        start = row.get("protein1")
        end = row.get("protein2")
        if start is None or end is None:
            continue

        if start not in nodes_in:

            s_node[NT.id] = int(next_id)
            next_id += 1
            s_node[NT.name] = start.split(".")[1]

            # get uniprot id(s)
            alias = alias_table.loc[start]
            s_node["uniprot"] = list(
                alias.loc[alias["source"] == "Ensembl_UniProt_AC"].get("alias")
            )
            s_node["stringdb_description"] = description_table.loc[start].get(
                "annotation"
            )

            nodes_in[start] = s_node[NT.id]
            network[VRNE.nodes].append(s_node)

        if end not in nodes_in:

            e_node[NT.id] = int(next_id)
            next_id += 1
            e_node[NT.name] = end
            # get uniprot id(s)
            alias = alias_table.loc[end]
            e_node["uniprot"] = list(
                alias.loc[alias["source"] == "Ensembl_UniProt_AC"].get("alias").values
            )
            e_node[NT.species] = species
            annotation = description_table.loc[end].get("annotation")
            if annotation != "annotation not available":
                e_node["stringdb_description"] = annotation

            nodes_in[end] = e_node[NT.id]
            network[VRNE.nodes].append(e_node)

        link[LiT.id] = idx
        link[LiT.start] = nodes_in[start]
        link[LiT.end] = nodes_in[end]

        for key in ev_columns:
            value = int(row.get(key))
            if value > 0:
                if key == "experimental":
                    key = st.Evidences.stringdb_experiments
                elif key == "database":
                    key = st.Evidences.stringdb_databases
                else:
                    key = f"stringdb_{key}"

                link[key] = value / 1000

        network[VRNE.links].append(link)

        util.printProgressBar(idx + 1, last, prefix="Progress:", suffix="Complete")
    print("#Links:", len(network[VRNE.links]))
    print("#Nodes:", len(network[VRNE.nodes]))

    with open(os.path.join(st._PROJECTS_PATH, organism) + ".VRNetz", "w") as f:
        json.dump(network, f)


if __name__ == "__main__":
    write_VRNetz(st.Organisms.human, "STRING")
