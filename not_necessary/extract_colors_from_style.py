from re import M

import bs4
from bs4 import BeautifulSoup as BS
from PIL import ImageColor


def get_node_mapping(file: str) -> dict or None:
    with open(file) as f:
        soup = BS(f, "xml")
    tag = soup.node
    prop = tag.find("visualProperty", {"name": "NODE_FILL_COLOR"})
    default_color = prop.attrs["default"]
    default_color = ImageColor.getcolor(default_color, "RGB") + (255,)
    color_mapping = {"default": default_color}
    mapping_types = {
        "discreteMapping": get_discrete_mapping,
        "passthroughMapping": get_passthrough_mapping,
        "continuousMapping": get_continuous_mapping,
    }
    for mapping in mapping_types:
        if prop.find(mapping) is not None:
            color_mapping = mapping_types[mapping](color_mapping, prop)
            return color_mapping
    return None


def get_discrete_mapping(color_mapping: dict, prop: bs4.element.Tag) -> dict or None:
    """Extracts the discrete color mappings of the node from a sytles.xml file and returns a dictionary of the mappings."""
    color_mapping["type"] = "discrete"
    discreteMapping = prop.find("discreteMapping")
    for node in discreteMapping.children:
        if isinstance(node, bs4.element.Tag):
            name = node["attributeValue"]
            color = node["value"]
            color_mapping[name] = ImageColor.getcolor(color, "RGB") + (255,)
    return color_mapping


def get_passthrough_mapping(color_mapping: dict, prop: bs4.element.Tag) -> dict or None:
    """Extracts the passthrough color mappings of the node from a sytles.xml file and returns a dictionary of the mappings."""
    color_mapping["type"] = "passthrough"
    passthroughMapping = prop.find("passthroughMapping")
    color_mapping["column"] = passthroughMapping.attrs["attributeName"]
    return color_mapping


def get_continuous_mapping(color_mapping: dict, prop: bs4.element.Tag) -> dict or None:
    """Extracts the continuous color mappings of the node from a sytles.xml file and returns a dictionary of the mappings."""
    color_mapping["type"] = "continuous"
    continuesMapping = prop.find("continuousMapping")
    color_mapping["column"] = continuesMapping.attrs["attributeName"]
    for point in continuesMapping.children:
        if isinstance(point, bs4.element.Tag):
            values = [
                point.attrs["equalValue"],
                point.attrs["lesserValue"],
                point.attrs["greaterValue"],
            ]
            for i, color in enumerate(values):
                values[i] = ImageColor.getcolor(color, "RGB") + (255,)
            color_mapping[float(point.attrs["attrValue"])] = values
    return color_mapping


if __name__ == "__main__":
    file = "/Users/till/Desktop/styles_1000_nodes.xml"
    file = "/Users/till/Documents/UNI/Master_Bioinformatik-Universität_Wien/3.Semester/Masterthesis/STRING-VRNetzer/static/styles/STRING network - Alzheimers disease.xml"
    import sys

    if len(sys.argv) > 1:
        file = sys.argv[1]

    color_mapping = get_node_mapping(file)
    print(color_mapping)
