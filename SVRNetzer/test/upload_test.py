import os
import sys

sys.path.append("/Users/till/Documents/Playground/STRING-VRNetzer")
from SVRNetzer.main import main


def upload_100_alz():
    network = "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/100_alzheimer.VRNetz"
    arg = [
        "",
        "project",
        network,
        "None",
        "None",
        "None",
        "WebGL_Test",
        "False",
        "False",
        "True",
    ]
    main(arg=arg)


if __name__ == "__main__":
    upload_100_alz()
