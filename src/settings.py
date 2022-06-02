import os

_PROJECTS_PATH = os.path.abspath(f"{__file__}/../../static/projects")
_NETWORKS_PATH = os.path.abspath(f"{__file__}/../../static/networks")
os.makedirs(_PROJECTS_PATH, exist_ok=os.X_OK)
os.makedirs(_NETWORKS_PATH, exist_ok=os.X_OK)
