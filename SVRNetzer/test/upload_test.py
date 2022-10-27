import os
import sys

from main import main


def upload_100_alz():
    # FIXME: Change of color will just color the first edge instead of moving the edges.
    network = "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/100_alzheimer.VRNetz"
    arg = [
        "",
        "project",
        network,
        "cg_local_umap",
        "None",
        "None",
        "WebGL_Test",
        "True",
        "True",
        "True",
    ]
    main(arg=arg)


if __name__ == "__main__":
    upload_100_alz()
