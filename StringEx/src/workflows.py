import json
import logging
import os

from .converter import VRNetzConverter
# from .cytoscape_parser import CytoscapeParser
from .layouter import Layouter
from .map_small_on_large import map_source_to_target
from .settings import _NETWORKS_PATH, _PROJECTS_PATH, UNIPROT_MAP, Organisms
# from .settings import VRNetzElements as VRNE
# from .string_commands import (StringCompoundQuery, StringDiseaseQuery,
#                               StringProteinQuery, StringPubMedQuery)
from .uploader import Uploader

# import networkx as nx


# from extract_colors_from_style import get_node_mapping


logger = logging.getLogger("VRNetzer Cytoscape App")
logger.setLevel(logging.DEBUG)

def VRNetzer_upload_workflow(request):
    """Used from the StringEX/uploadfiles route"""
    print("Starting upload of VRNetz...")
    stringify, write_VRNetz,gen_layout,algo = False, False, False, None
    form = request.form.to_dict()
    network = request.files.getlist("vrnetz")[0].read().decode("utf-8")
    network = json.loads(network)

    project_name = ""

    if form["namespace"] == "New":
        project_name = form["new_name"]

    else:
        project_name = form["existing_namespace"]
    if not project_name:
        return "namespace fail"
    # print(form.keys())
    if algo in form:
        algo = form["algo"]

    tags = {"stringify":stringify,
     "write":write_VRNetz,"calc_lay":gen_layout}
    for key,_ in tags.items():
        if key in form:
            tags[key] = True
    stringify, write_VRNetz,gen_layout = tags["stringify"], tags["write"], tags["calc_lay"]        
    # create layout
    layouter = apply_layout_workflow(network, layout_algo=algo, stringify=stringify,gen_layout=gen_layout)
    network = layouter.network

    # upload network
    uploader = Uploader(network, p_name=project_name, stringify=stringify)
    state = uploader.upload_files(network)
    if write_VRNetz:
        outfile = f"{_NETWORKS_PATH}/{project_name}_processed.VRNetz"
        print(f"processed network saved at:{outfile}")
        with open(outfile, "w") as f:
            json.dump(network, f)
        logging.info(f"Saved network as {outfile}")
    if stringify:
        uploader.stringify_project()
        print("stringified")
        logging.info(f"Layouts stringified: {project_name}")
    return state

def VRNetzer_map_workflow(request):
    """Used from the StringEX/mapfiles route"""

    print("Starting mapping of VRNetz...")

    form = request.form.to_dict()
    f_src_network = request.files.getlist("vrnetz")[0]
    src_network = f_src_network.read().decode("utf-8")
    src_network = json.loads(src_network)
    
    organ = form.get("organism")
    f_organ = Organisms.get_file_name(organ)
    f_organ = os.path.join(_PROJECTS_PATH, f_organ)
    trg_network = json.loads(organ)

    project_name = form.get("project_name")
    if project_name is None or project_name == "":
        src_name = os.path.split(f_src_network.filename)[1].split(".")[0]
        trg_name = organ.replace(".","_")
        project_name = f"{src_name}_on_{trg_name}"

    destination = os.path.join(_PROJECTS_PATH, project_name)
    try:
        map_source_to_target(src_network, trg_network, destination)
        html = (f'<a style="color:green;">SUCCESS: network {f_src_network.filename} mapped on {organ} saved as project {project_name} </a>'
        f"<br>"+
        f'<input type="submit" value="Preview" id="upload_preview" style="height: 50px; width: 150px;">'+
        "<script>"+
        "$('#reload').on('click', function() {"+
        f"var url = window.location.href.split('&')[0] + '&project={project_name}'"+
        f"window.location.href = url;"+
        "});"
        f"</script>'")
    except Exception as e:
        html = f'<a style="color:red;">ERROR: {e}</a>'
    return html

def apply_layout_workflow(
    network: str,
    gen_layout: bool = True,
    layout_algo: str = None,
    cy_layout: bool = True,
    stringify: bool = True,
) -> Layouter:
    layouter = Layouter()
    if type(network) is dict:
        layouter.network = network
        nodes = layouter.network["nodes"]
        links = layouter.network["links"]
        layouter.gen_graph(nodes, links)
    else:

        layouter.read_from_vrnetz(network)
        logger.info(f"Network extracted from: {network}")

    if gen_layout:
        layouter.apply_layout(layout_algo)
        if layout_algo is None:
            layout_algo = "spring"
        logger.info(f"Layout algorithm {layout_algo} applied!")
    # Correct Cytoscape positions to be positive.
    if cy_layout:
        layouter.correct_cytoscape_pos()
        logger.info(f"2D layout created!")
    if stringify:
        layouter.gen_evidence_layouts()
    return layouter



def create_project_workflow(
    network: dict,
    project_name: str,
    projects_path: str = _PROJECTS_PATH,
    skip_exists: bool = False,
    keep_tmp: bool = False,
    cy_layout: bool = True,
    stringifiy: bool = True,
):
    """Uses a layout to generate a new VRNetzer Project."""
    uploader = Uploader(network, project_name, skip_exists, stringifiy, projects_path)
    state = uploader.upload_files(network)
    if keep_tmp:
        outfile = f"{_NETWORKS_PATH}/{project_name}_with_3D_Coords.VRNetz"
        print(f"OUTFILE:{outfile}")
        with open(outfile, "w") as f:
            json.dump(network, f)
        logging.info(f"Saved network as {outfile}")
    if stringifiy and cy_layout:
        uploader.stringify_project()
        logging.info(f"Layouts stringified: {project_name}")
    logging.info(f"Project created: {project_name}")
    return state


def map_workflow(small_net: str, large_net: str, destination: str) -> None:
    """Maps a small network onto a large network."""
    map_source_to_target(small_net, large_net, destination)


def convert_workflow(
    node_list: str, edge_list: str, uniprot_mapping=None, project=None
) -> str:
    """Converts a network from a edge and node list to a .VRNetz file."""
    if uniprot_mapping is None:
        uniprot_mapping = UNIPROT_MAP
    if project is None:
        project = "NA"
    output = os.path.join(_NETWORKS_PATH, project)
    converter = VRNetzConverter(node_list, edge_list, uniprot_mapping, project)
    converter.convert()
    return output

# def apply_style_workflow(graph: nx.Graph, style: str) -> nx.Graph:
#     color_mapping = get_node_mapping(style)
#     if color_mapping is None:
#         return graph
#     mapping_type = color_mapping["type"]
#     logger.info(
#         f"Color mapping extracted from: {style}.xml. Mapping Type: {mapping_type}"
#     )
#     graph = colorize_nodes(graph, color_mapping)
#     logger.info(f"Colored nodes according to color mapping.")
#     return graph

# def protein_query_workflow(
#     parser: CytoscapeParser, p_query: list[str], **kwargs
# ) -> None:
#     """Fetches a network for given protein query."""
#     query = StringProteinQuery(query=p_query, **kwargs)
#     logger.info(f"Command as list:{query.cmd_list}")
#     parser.exec_cmd(query.cmd_list)


# def disease_query_workflow(parser: CytoscapeParser, disease: str, **kwargs) -> None:
#     """Fetches a network for given disease query."""
#     query = StringDiseaseQuery(disease=disease, **kwargs)
#     logger.info(f"Command as list:{query.cmd_list}")
#     parser.exec_cmd(query.cmd_list)


# def compound_query_workflow(
#     parser: CytoscapeParser, query: list[str], **kwargs
# ) -> None:
#     """Fetches a network for given compound query."""
#     query = StringCompoundQuery(query=query, **kwargs)
#     logger.info(f"Command as list:{query.cmd_list}")
#     parser.exec_cmd(query.cmd_list)


# def pubmed_query_workflow(parser: CytoscapeParser, pubmed: list[str], **kwargs) -> None:
#     """Fetches a network for given pubmed query."""
#     query = StringPubMedQuery(pubmed=pubmed, **kwargs)
#     logger.info(f"Command as list:{query.cmd_list}")
#     parser.exec_cmd(query.cmd_list)
#     print(query.cmd_list)


# def export_network_workflow(
#     parser: CytoscapeParser,
#     filename: str = None,
#     network: str = None,
#     keep_output: bool = True,
#     layout_algo: str = None,
#     **kwargs,
# ) -> tuple[Layouter, str]:
#     """Exports a network as GraphML file, generates a 3D layout."""
#     networks = parser.get_network_list()
#     if network is None:
#         network = list(networks.keys())[0]
#     if filename is None:
#         filename = network
#     filename = filename.replace(" ", "_")
#     network_loc = f"{_NETWORKS_PATH}/{filename}"
#     network_file = f"{network_loc}.VRNetz"

#     parser.export_network(filename=network_loc)
#     logger.info(f"Network exported: {network}")

#     # generate a 3D layout
#     layouter = apply_layout_workflow(f"{network_loc}.VRNetz", layout_algo)

#     # if keep_output is False, we remove the tmp GraphML file
#     if not keep_output:
#         os.remove(network_file)
#         logger.info(f"Removed tmp file: {network_file}")

#     return layouter, filename


# TODO: Networkx export with separate table export. Does not work do fails in matching node/edge names to SUIDs
# def parse_network(parser: CytoscapeParser, network_index=None, **kwargs):
#     if network_index is None:
#         network_index = 0
#     networks = parser.get_network_list()
#     network = list(networks.keys())[network_index]
#     graph = parser.get_networkx_network(network)
#     # node_columns, edge_columns = parser.export_table(network)
#     nx.draw(graph)
#     plt.show()


# TODO directly create a networkx network
