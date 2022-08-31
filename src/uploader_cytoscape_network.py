import json
import os
from re import A
from typing import List

import networkx as nx
from flask import jsonify
from PIL import Image

from GlobalData import sessionData
from settings import _STATIC_PATH


def makeProjectFolders(name: str, projects_path: str = "static/projects"):
    path = f"{projects_path}/{name}"
    pfile = {}
    pfile["name"] = name
    pfile["layouts"] = []
    pfile["layoutsRGB"] = []
    pfile["links"] = []
    pfile["linksRGB"] = []
    pfile["selections"] = []

    os.makedirs(path, exist_ok=os.X_OK)
    os.makedirs(path + "/layouts", exist_ok=os.X_OK)
    os.makedirs(path + "/layoutsl", exist_ok=os.X_OK)
    os.makedirs(path + "/layoutsRGB", exist_ok=os.X_OK)
    os.makedirs(path + "/links", exist_ok=os.X_OK)
    os.makedirs(path + "/linksRGB", exist_ok=os.X_OK)

    with open(path + "/pfile.json", "w") as outfile:
        json.dump(pfile, outfile)

    print("Successfully created directories in %s " % path)


def loadProjectInfo(name: str, projects_path: str = "static/projects"):
    folder = f"{projects_path}/{name}/"
    layoutfolder = folder + "layouts"
    layoutRGBfolder = folder + "layoutsRGB"
    linksRGBfolder = folder + "linksRGB"
    linkfolder = folder + "links"

    if os.path.exists(folder):

        layouts = [name for name in os.listdir(layoutfolder)]
        layoutsRGB = [name for name in os.listdir(layoutRGBfolder)]
        links = [name for name in os.listdir(linkfolder)]
        linksRGB = [name for name in os.listdir(linksRGBfolder)]

        return jsonify(
            layouts=layouts, layoutsRGB=layoutsRGB, links=links, linksRGB=linksRGB
        )
    else:
        return "no such project"


def loadAnnotations(name: str, projects_path: str = "static/projects"):
    """Return all annotations corresponding to a project name."""
    namefile = f"{projects_path}/{name}/names.json"
    f = open(namefile)
    data = json.load(f)
    return data


def listProjects(projects_path: str = "static/projects"):
    """Returns a list of all projects."""
    projects_path
    os.makedirs(projects_path, exist_ok=os.X_OK)
    sub_folders = [
        name
        for name in os.listdir(projects_path)
        if os.path.isdir(os.path.join(projects_path, name))
    ]
    # print(sub_folders)
    return sub_folders


# TODO other name for variable filename. maybe Layout name
def makeNodeTex(
    project: str,
    filename: str,
    nodes: dict,
    projects_path: str = "static/projects",
    skip_exists=True,
    skip_attr=["pos", "color", "selected"],
    coord_column="VRNetzer_pos",
) -> str:
    """Generates Node textures from a dictionary of nodes."""
    elem = len(nodes)
    hight = 128 * (int(elem / 16384) + 1)

    size = 128 * hight
    path = f"{projects_path}/{project}"

    texh = [(0, 0, 0)] * size
    texl = [(0, 0, 0)] * size
    texc = [(0, 0, 0, 0)] * size

    new_imgh = Image.new("RGB", (128, hight))
    new_imgl = Image.new("RGB", (128, hight))
    new_imgc = Image.new("RGBA", (128, hight))
    attrlist = {}
    attrlist["names"] = []
    for i, elem in enumerate(nodes):
        position = elem[coord_column]
        name = ["NA"]
        if "stringdb_canonical name" in elem.keys():
            name = elem["stringdb_canonical name"]
        elif "display name" in elem.keys():
            gene_name = elem["display name"]
            name = f"GENENAME={gene_name}"
        attrlist["names"].append([name])
        attributes = [k for k in elem.keys() if k not in skip_attr]
        for attr in attributes:
            if not attr in attrlist:
                attrlist[attr] = []
            attrlist[attr].append([elem[attr]])
        coords = [0, 0, 0]  # x,y,z
        color = [255, 0, 255, 255]  # r,g,b,a

        if "node_color" in elem.keys():
            if isinstance(elem["node_color"], list):
                color = elem["node_color"]
        for d, _ in enumerate(position):
            coords[d] = int(float(position[d]) * 65280)
        high = [value // 255 for value in coords]
        low = [value % 255 for value in coords]

        texh[i] = tuple(high)
        texl[i] = tuple(low)
        texc[i] = tuple(color)
    new_imgh.putdata(texh)
    new_imgl.putdata(texl)
    new_imgc.putdata(texc)

    with open(path + "/names.json", "w") as outfile:
        json.dump(attrlist, outfile)
    pathXYZ = path + "/layouts/" + filename + "XYZ.bmp"
    pathXYZl = path + "/layoutsl/" + filename + "XYZl.bmp"
    pathRGB = path + "/layoutsRGB/" + filename + "RGB.png"

    if not skip_exists:
        new_imgh.save(pathXYZ)
        new_imgl.save(pathXYZl)
        new_imgc.save(pathRGB, "PNG")
        return (
            '<a style="color:green;">SUCCESS </a>' + filename + " Node Textures Created"
        )

    if os.path.exists(pathXYZ):
        return (
            '<a style="color:red;">ERROR </a>'
            + filename
            + " Nodelist already in project"
        )
    else:
        new_imgh.save(pathXYZ)
        new_imgl.save(pathXYZl)
        new_imgc.save(pathRGB, "PNG")
        return (
            '<a style="color:green;">SUCCESS </a>' + filename + " Node Textures Created"
        )


# TODO other name for variable filename. maybe Layout name
def makeLinkTex(
    project: str,
    filenname: str,
    edges: dict,
    nodes: list,
    projects_path: str = "static/projects",
    skip_exists=True,
) -> str:
    """Generate a Link texture from a dictionary of edges."""

    hight = 512
    path = f"{projects_path}/{project}"

    texl = [(0, 0, 0)] * 1024 * hight
    texc = [(0, 0, 0, 0)] * 512 * hight
    new_imgl = Image.new("RGB", (1024, hight))
    new_imgc = Image.new("RGBA", (512, hight))
    node_ids = {}
    for i, node in enumerate(nodes):
        node_ids[int(node)] = i
    # observed_edges = []
    for i, edge in enumerate(edges):
        edge = edges[edge]
        source = node_ids[int(edge["source"])]
        sink = node_ids[int(edge["sink"])]
        # # Prevent duplicate edges
        # if [source, sink] in observed_edges or [sink, source] in observed_edges:
        #     continue
        # else:
        #     observed_edges.append([source, sink])

        sx = source % 128
        syl = source // 128 % 128
        syh = source // 16384

        ex = sink % 128
        eyl = sink // 128 % 128
        eyh = sink // 16384

        color = [0, 100, 255, 255]
        if "color" in edge.keys():
            if isinstance(edge["color"], tuple):
                color = edge["color"]
        pixell1 = (sx, syl, syh)
        pixell2 = (ex, eyl, eyh)
        pixelc = tuple(color)

        if i >= 262144:
            break

        texl[i * 2] = pixell1
        texl[i * 2 + 1] = pixell2
        texc[i] = pixelc
    # with open(os.path.join(path, filenname + "_texl"), "w") as f:
    #     f.write(str(texl))
    # with open(os.path.join(path, filenname + "_texc"), "w") as f:
    #     f.write(str(texc))
    new_imgl.putdata(texl)
    new_imgc.putdata(texc)
    pathl = path + "/links/" + filenname + "XYZ.bmp"
    pathRGB = path + "/linksRGB/" + filenname + "RGB.png"

    # new_imgl.save(pathl, "PNG")
    # new_imgc.save(pathRGB, "PNG")
    # return '<a style="color:green;">SUCCESS </a>' + filenname + " Link Textures Created"
    if not skip_exists:
        new_imgl.save(pathl, "PNG")
        new_imgc.save(pathRGB, "PNG")
        return (
            '<a style="color:green;">SUCCESS </a>'
            + filenname
            + " Link Textures Created"
        )

    if os.path.exists(pathl):
        return (
            '<a style="color:red;">ERROR </a>'
            + filenname
            + " linklist already in project"
        )
    else:
        new_imgl.save(pathl, "PNG")
        new_imgc.save(pathRGB, "PNG")
        return (
            '<a style="color:green;">SUCCESS </a>'
            + filenname
            + " Link Textures Created"
        )


# TODO other name for variable filename. maybe Layout name
def upload_files(
    project: str,
    filename: str,
    network: dict,
    projects_path: str = "static/projects",
    skip_exists: bool = True,
    evidences: dict = None,
):
    project = clean_filename(project)
    filename = clean_filename(filename)
    ingored_elements = ["data_type", "amount"]
    nodes_data = {
        node: data
        for node, data in network["nodes"].items()
        if node not in ingored_elements
    }
    edges_data = {
        edge: data
        for edge, data in network["edges"].items()
        if edge not in ingored_elements
    }
    """Generates textures and upload the needed network files."""
    if evidences is None:
        evidences = {
            "any": (200, 200, 200, 255),
            "stringdb_interspecies": (125, 225, 240, 255),
            "stringdb_experiments": (255, 100, 160, 255),
            "stringdb_coexpression": (50, 50, 50, 255),
            "stringdb_databases": (90, 255, 255, 255),
            "stringdb_neighborhood": (0, 255, 0, 255),
            "stringdb_cooccurence": (0, 0, 255, 255),
            "stringdb_fusion": (255, 0, 0, 255),
            "stringdb_similarity": (255, 255, 255, 255),
        }
    prolist = listProjects(projects_path)
    # GET LAYOUT
    if not skip_exists:
        makeProjectFolders(project, projects_path=projects_path)
    else:
        if project in prolist:

            print("project exists")
        else:
            # Make Folders
            makeProjectFolders(project, projects_path=projects_path)

    folder = f"{projects_path}/{project}/"
    pfile = {}

    with open(folder + "pfile.json", "r") as json_file:
        pfile = json.load(json_file)
    json_file.close()

    state = ""
    # Create 2D Layout of Cytoscape coordinates node texture
    _2dlayout_filename = f"{filename}_2d"
    output = makeNodeTex(
        project,
        _2dlayout_filename,
        nodes_data.values(),
        projects_path,
        skip_exists,
        coord_column="node_Cytoscape_pos",
    )
    state += f"{state}<br>{output}"
    pfile["layouts"].append(f"{_2dlayout_filename}XYZ")
    pfile["layoutsRGB"].append(f"{_2dlayout_filename}RGB")
    pfile["links"].append(f"anyXYZ")
    pfile["linksRGB"].append(f"anyRGB")

    # layout_files = request.files.getlist("layouts")  # If a network has multiple layouts
    # Create 3D Layout node textures
    state += f"{state}<br>{makeNodeTex(project, filename, nodes_data.values(), projects_path, skip_exists)}"
    # print(contents)
    # x = validate_layout(contents.split("\n"))
    # print("layout errors are", x)
    # if x[1] == 0:

    # Upload.upload_layouts(namespace, layout_files)
    # For each evidence type, create a texture and upload it
    for evidence in evidences:
        edges = edges_data.copy()
        if not evidence == "any":
            edges = {
                edge: data for edge, data in edges.items() if evidence in data.keys()
            }
        # Skip This evidence if there are not edges for this evidence
        if len(edges) == 0:
            continue

        # Color each link with the color of the evidence
        for edge in edges:
            edges[edge]["color"] = evidences[evidence]

        # Add node layout to pflie for this link layout
        pfile["layouts"].append(f"{filename}XYZ")
        pfile["layoutsRGB"].append(f"{filename}RGB")

        # Add link layout to pfile
        pfile["links"].append(f"{evidence}XYZ")
        pfile["linksRGB"].append(f"{evidence}RGB")

        # Generate link texture
        state += f"{state}<br>{makeLinkTex(project,evidence,edges,nodes_data.keys(),projects_path,skip_exists)}"

    # update the projects file
    with open(folder + "pfile.json", "w") as json_file:
        json.dump(pfile, json_file)

    global sessionData
    sessionData["proj"] = listProjects(projects_path)

    return state


def prepare_networkx_network(G: nx.Graph, positions: dict = None) -> tuple[dict, dict]:
    """Transforms a basic networkx graph into a correct data structure to be uploaded by the Cytoscape uploader. If the positions are not given, the positions are calculated using the spring layout algorithm of networkx."""
    if positions is None:
        positions = nx.spring_layout(G, dim=3)
    for node in G.nodes():
        nx.set_node_attributes(
            G,
            {
                "pos": positions[node],
                "uniprotide": node,
                "display_name": "Gene Name of the Protein",
            },
        )
    return G


def clean_filename(name: str) -> str:
    """Cleans the project name to be used in the file names."""
    name = name.replace(" ", "_")
    name = name.replace("/", "_")
    name = name.replace("'", "")
    name = name.replace("´", "")
    name = name.replace("`", "")
    name = name.replace("'", "")
    name = name.replace("“", "")
    name = name.replace(",", "_")
    name = name.replace(".", "_")
    name = name.replace("-", "_")
    name = name.replace("–", "_")
    name = name.replace("#", "_")
    return name


if __name__ == "__main__":
    _FILE_PATH = os.path.abspath(f"{__file__}/../../")
    _PROJECTS_PATH = f"{_FILE_PATH}/static/projects"
    sessionData["proj"] = listProjects(_PROJECTS_PATH)
    print(sessionData["proj"])
