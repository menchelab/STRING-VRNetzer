import json

from SVRNetzer.util.settings import VRNetzElements as VRNE

file = "/Users/till/Documents/Playground/STRING-VRNetzer/static/networks/convert_test.VRNetz"
with open(file, "r") as json_file:
    data = json.load(json_file)
print(data[VRNE.link_layouts])
