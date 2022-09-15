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


class EdgeTags:
    source = "source"
    sink = "sink"
    color = "color"


class Evidences:
    stringdb_textmining = "stringdb_textmining"
    stringdb_experiments = "stringdb_experiments"
    stringdb_coexpression = "stringdb_coexpression"
    stringdb_databases = "stringdb_databases"
    stringdb_neighborhood = "stringdb_neighborhood"
    stringdb_cooccurence = "stringdb_cooccurence"
    stringdb_fusion = "stringdb_fusion"
    stringdb_similarity = "stringdb_similarity"

    @staticmethod
    def get_default_scheme():
        """Return a dictionary with the color scheme for each evidence."""
        return {
            "any": (200, 200, 200, 255),  # Color for all evidences active
            Evidences.stringdb_textmining: (199, 234, 70, 255),
            # "stringdb_interspecies": (125, 225, 240, 255), # Not Used anywhere
            Evidences.stringdb_experiments: (254, 0, 255, 255),
            Evidences.stringdb_coexpression: (50, 50, 50, 255),
            Evidences.stringdb_databases: (0, 255, 255, 255),
            Evidences.stringdb_neighborhood: (0, 255, 0, 255),
            Evidences.stringdb_cooccurence: (0, 0, 255, 255),
            Evidences.stringdb_fusion: (255, 0, 0, 255),
            Evidences.stringdb_similarity: (157, 157, 248, 255),
        }
