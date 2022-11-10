import logging
import os
import sys

try:
    from pip._internal.operations import freeze
except ImportError:  # pip < 10.0
    from pip.operations import freeze

_WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
_EXTENSION_PATH = os.path.join(_WORKING_DIR, "..", "..")
_VRNETZER_PATH = os.path.join(_EXTENSION_PATH, "..")

_STATIC_PATH = os.path.join(_VRNETZER_PATH, "static")
_PROJECTS_PATH = os.path.join(_STATIC_PATH, "projects")
_NETWORKS_PATH = os.path.join(_STATIC_PATH, "networks")

_FLASK_TEMPLATE_PATH = os.path.join(_WORKING_DIR, "..", "templates")
_FLASK_STATIC_PATH = os.path.join(_WORKING_DIR, "..", "static")
_VRNETZER_PATH = os.path.join(_WORKING_DIR, "..", "..")
_VRNETZER_TEMPLATE_PATH = os.path.join(_VRNETZER_PATH, "templates")
# _STYLES_PATH = os.path.join(_STATIC_PATH, "styles")
os.makedirs(_PROJECTS_PATH, exist_ok=os.X_OK)
os.makedirs(_NETWORKS_PATH, exist_ok=os.X_OK)
# os.makedirs(_STYLES_PATH, exist_ok=os.X_OK)

UNIPROT_MAP = os.path.join(_STATIC_PATH, "uniprot_mapping.csv")
HELP_TEXT = (
    "Usage:\n"
    + "main.py query <query type=[protein/disease/compound/pubmed]> <query> <opt:cutoff> <opt:limit> <opt:species> <opt:taxonID>"
    + "\n"
    "or\n"
    + "main.py export <network> <filename> <opt:KeepTmp> <opt:*> <opt:overwrite_file>"
    + "\n"
    + "or\n"
    + "main.py project <network> <opt:layout_algo> <opt:keep_temp> <opt:skip_exists> <opt:project_name> <opt:gen_layout> <opt:cy_layout> <opt:stringify>"
    + "\n"
    + "or\n"
    + "main.py names"
    + "\n"
    + "or\n"
    + "main.py map <source_network> <target_network> <opt:output_name>"
    + "\n"
    + "or\n"
    + "main.py convert <node_list> <edge_list> <opt:uniprot_mapping> <opt:project_name>"
    + "\n"
    + "possible algorithms:\n"
    + "spring, kamada_kawai, cg_local_tsne, cg_local_umap, cg_global_tsne, cg_global_umap, cg_importance_tsne, cg_importance_umap"
)
logger = logging.getLogger("StringEx")
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Tags
class LayoutTags:
    position = "p"
    color = "c"
    size = "s"
    id = "id"
    cy_layout = "cy"
    name = "n"
    _3d = "3d"
    string_3d = "st3d"
    string_3d_no_z = "st2d"


class NodeTags:
    layouts = "layouts"
    vrnetzer_pos = "vp"
    node_color = "c"
    name = "n"
    suid = "SUID"
    description = "description"
    sequence = "sequence"
    species = "species"
    ppi_id = "ppi_id"
    id = "id"
    attr_lst = "attrlist"
    uniprot = "uniprot"


class StringTags:
    stringdb_canoncial_name = "stringdb_canonical name"
    stringdb_sequence = "stringdb_sequence"
    stringdb_description = "stringdb_description"
    stringdb_species = "stringdb_species"


class ProjectTag:
    layouts = "layouts"
    layouts_rgb = "layoutsRGB"
    links = "links"
    links_rgb = "linksRGB"


class AttrTags:
    names = "names"


class LinkTags:
    id = "id"
    start = "s"
    end = "e"
    suid = "SUID"
    ppi_id = "ppi_id"
    layouts = "c"


class VRNetzElements:
    nodes = "nodes"
    links = "links"
    node_layouts = "layouts"  # edge layout
    link_layouts = "l_layout"  # link layout


class LayoutAlgroithms:
    spring = "spring"

    kamada_kawai = "kamada_kawai"
    all_algos = [spring, kamada_kawai]
    cartoGRAPH = "cg"
    cartoGRAPH_local = "local"
    cartoGRAPH_global = "global"
    cartoGRAPH_importance = "importance"
    cartoGRAPH_tsne = "tsne"
    cartoGRAPH_umap = "umap"

    if "cartoGRAPHs" in [module.split("=")[0] for module in list(freeze.freeze())]:
        all_algos += [
            f"{cartoGRAPH}_{cartoGRAPH_local}_{cartoGRAPH_tsne}",
            f"{cartoGRAPH}_{cartoGRAPH_local}_{cartoGRAPH_umap}",
            f"{cartoGRAPH}_{cartoGRAPH_global}_{cartoGRAPH_tsne}",
            f"{cartoGRAPH}_{cartoGRAPH_global}_{cartoGRAPH_umap}",
            f"{cartoGRAPH}_{cartoGRAPH_importance}_{cartoGRAPH_tsne}",
            f"{cartoGRAPH}_{cartoGRAPH_importance}_{cartoGRAPH_umap}",
        ]


class Evidences:
    any = "any"
    stringdb_textmining = "stringdb_textmining"
    stringdb_experiments = "stringdb_experiments"
    stringdb_coexpression = "stringdb_coexpression"
    stringdb_databases = "stringdb_databases"
    stringdb_neighborhood = "stringdb_neighborhood"
    stringdb_cooccurrence = "stringdb_cooccurrence"
    stringdb_fusion = "stringdb_fusion"
    stringdb_similarity = "stringdb_similarity"

    @staticmethod
    def get_default_scheme() -> dict:
        """Return a dictionary with the color scheme for each evidence."""
        ev = {
            Evidences.any: (
                200,
                200,
                200,
                255,
            ),  # Color for all evidences active #c8c8c8
            Evidences.stringdb_textmining: (199, 234, 70, 255),  # #c6ea46
            # "stringdb_interspecies": (125, 225, 240, 255), # Not Used anywhere
            Evidences.stringdb_experiments: (254, 0, 255, 255),  # ##ff00ff
            Evidences.stringdb_coexpression: (50, 50, 50, 255),  # #323232
            Evidences.stringdb_databases: (0, 255, 255, 255),  # #00ffff
            Evidences.stringdb_neighborhood: (0, 255, 0, 255),  # #00ff00
            Evidences.stringdb_cooccurrence: (0, 0, 255, 255),  # #0000ff
            Evidences.stringdb_fusion: (255, 0, 0, 255),  # #ff0000
            Evidences.stringdb_similarity: (157, 157, 248, 255),  # #9d9df8
        }
        return ev


class Organisms:
    human = "H.sapiens"
    mouse = "M.musculus"
    yeast = "S.cerevisiae"
    worm = "C.elegans"
    fly = "D.melanogaster"
    arabidopsis = "A.thaliana"
    zebrafish = "D.rerio"
    rat = "R.norvegicus"
    ecoli = "E.coli"
    all_organisms = sorted(
        [human, mouse, yeast, worm, fly, arabidopsis, zebrafish, rat, ecoli]
    )

    @staticmethod
    def get_tax_ids(organism):
        """Return the tax id for the organism."""
        tax_ids = {
            Organisms.human: 9606,
            Organisms.mouse: 10090,
            Organisms.rat: 10116,
            Organisms.zebrafish: 7955,
            Organisms.fly: 7227,
            Organisms.worm: 6239,
            Organisms.yeast: 4932,
            Organisms.ecoli: 362663,
            Organisms.arabidopsis: 3702,
        }
        return tax_ids.get(organism)

    @staticmethod
    def get_scientific_name(organism):
        """Return the tax id for the organism."""
        tax_ids = {
            Organisms.human: "Homo sapiens",
            Organisms.mouse: "Mus musculus",
            Organisms.rat: "Rattus norvegicus",
            Organisms.zebrafish: "Danio rerio",
            Organisms.fly: "Drosophila melanogaster",
            Organisms.worm: "Caenorhabditis elegans",
            Organisms.yeast: "Saccharomyces cerevisiae",
            Organisms.ecoli: "Escherichia coli 536",
            Organisms.arabidopsis: "Arabidopsis thaliana",
        }
        return tax_ids.get(organism)

    # TODO: REMOVE BIOGRID IF NOT USED
    @staticmethod
    def get_file_name(organism: str) -> str:
        file_names = {
            Organisms.human: "new_ppi",
            Organisms.mouse: "string_mouse_ppi",
            Organisms.yeast: "string_yeast_ppi",
            Organisms.worm: "string_worm_ppi",
            Organisms.fly: "string_fly_ppi",
            Organisms.arabidopsis: "string_arabidopsis_ppi",
            Organisms.zebrafish: "string_zebrafish_ppi",
            Organisms.rat: "string_rat_ppi",
            Organisms.ecoli: "string_ecoli_ppi",
        }
        return file_names.get(organism)
