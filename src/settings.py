import os

_WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
_STATIC_PATH = os.path.join(_WORKING_DIR, "..", "static")
_PROJECTS_PATH = os.path.join(_STATIC_PATH, "projects")
_NETWORKS_PATH = os.path.join(_STATIC_PATH, "networks")
# _STYLES_PATH = os.path.join(_STATIC_PATH, "styles")

os.makedirs(_PROJECTS_PATH, exist_ok=os.X_OK)
os.makedirs(_NETWORKS_PATH, exist_ok=os.X_OK)
# os.makedirs(_STYLES_PATH, exist_ok=os.X_OK)


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
    # cartoGRAPHS_spring = "cartoGRPAHS_spring"


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
    def get_default_scheme():
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
