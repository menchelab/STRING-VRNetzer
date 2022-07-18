import os

_WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECTS_PATH = os.path.join(f"{_WORKING_DIR}", "..", "..", "static", "projects")
_NETWORKS_PATH = os.path.join(f"{_WORKING_DIR}", "..", "..", "static", "networks")
_STYLES_PATH = os.path.join(f"{_WORKING_DIR}", "..", "..", "static", "styles")
os.makedirs(_PROJECTS_PATH, exist_ok=os.X_OK)
os.makedirs(_NETWORKS_PATH, exist_ok=os.X_OK)
os.makedirs(_STYLES_PATH, exist_ok=os.X_OK)
