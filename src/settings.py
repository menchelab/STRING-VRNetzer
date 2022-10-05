import os

_WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
_STATIC_PATH = os.path.join(_WORKING_DIR, "..", "static")
_PROJECTS_PATH = os.path.join(_STATIC_PATH, "projects")
_NETWORKS_PATH = os.path.join(_STATIC_PATH, "networks")
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
    + "main.py project <network> <opt:layout_algo> <opt:KeepTmp> <opt:skip_exists> <opt:project_name> <opt:gen_layout> <opt:create_2d_layout>"
    + "\n"
    + "or\n"
    + "main.py names"
    + "\n"
    + "or\n"
    + "main.py map <source_network> <target_network> <opt:output_name>"
    + "\n"
    + "or\n"
    + "main.py convert <node_list> <edge_list> <opt:uniprot_mapping> <opt:project_name>"
)
# Tags
class NodeTags:
    vrnetzer_pos = "VRNetzer_pos"
    node_color = "node_color"
    display_name = "display name"
    suid = "SUID"
    description = "description"
    stringdb_canoncial_name = "stringdb_canonical name"
    stringdb_sequence = "stringdb_sequence"
    ppi_id = "ppi_id"


class EdgeTags:
    source = "source"
    sink = "sink"
    color = "color"
    suid = "SUID"
    ppi_id = "ppi_id"


class LayoutAlgroithms:
    spring = "spring"
    kamada_kawai = "kamada_kawai"
    cartoGRAPHs_global = "cartoGRPAHS_global"


class Evidences:
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
        return {
            "any": (200, 200, 200, 255),  # Color for all evidences active #c8c8c8
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
