import sys
from calendar import c

import bs4
from bs4 import BeautifulSoup as BS


def get_discrete_mapping(file: str) -> dict:
    with open(file) as f:
        soup = BS(f, "xml")
    tag = soup.node
    for prop in tag:
        try:
            if prop.attrs["name"] == "NODE_FILL_COLOR":
                myprop = prop
        except AttributeError:
            pass

    default_color = myprop.attrs["default"]
    color_mapping = {}
    for node in list(myprop.children)[1]:
        # TODO get node name, color
        if isinstance(node, bs4.element.Tag):
            name = node["attributeValue"]
            color = node["value"]
            color_mapping[name] = color
    print(len(color_mapping))
    return color_mapping


if __name__ == "__main__":
    file = "/Users/till/Desktop/styles_1000_nodes.xml"
    get_discrete_mapping(file)
