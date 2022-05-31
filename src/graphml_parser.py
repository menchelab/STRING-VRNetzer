import xml.etree.ElementTree as ET

_GRAPHML_URL = "{http://graphml.graphdrawing.org/xmlns}"


def parse_graphml_network(file: str):
    """Parses a Cytoscape network in a"""
    tree = ET.parse(file)
    root = tree.getroot()
    graphs = root.findall(f"{_GRAPHML_URL}graph")
    for graph in graphs:
        nodes = graph.findall(f"{_GRAPHML_URL}node")
        edges = graph.findall(f"{_GRAPHML_URL}edge")
        nodes_data = {}
        edges_data = {}
        for node in nodes:
            data = node.findall(f"{_GRAPHML_URL}data")
            data_dict = {}
            for d in data:
                _, v = d.items()[0]
                data_dict[v] = d.text
            # TODO This only works for String Networks! Maybe rename column before exporting?
            nodes_data[data_dict["SUID"]] = data_dict
        for edge in edges:
            data = edge.findall(f"{_GRAPHML_URL}data")
            data_dict = {k: v for k, v in edge.attrib.items()}
            for d in data:
                _, v = d.items()[0]
                data_dict[v] = d.text
            # TODO This might only work for String Networks! Maybe rename column before exporting?
            edges_data[data_dict["source"], data_dict["target"]] = data_dict
    return nodes_data, edges_data


def parse_xml_style(file: str):
    """Parses a Cytoscape style file"""
    pass


if __name__ == "__main__":
    parse_graphml_network("test.graphml")
