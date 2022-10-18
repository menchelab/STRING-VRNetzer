import json
import os

import numpy as np
from flask import jsonify
from PIL import Image

from .GlobalData import sessionData
from .settings import _PROJECTS_PATH
from .settings import AttrTags as AT
from .settings import EdgeTags as ET
from .settings import Evidences as EV
from .settings import LayoutTags as LT
from .settings import NodeTags as NT
from .settings import ProjectTag as PT
from .settings import VRNetzElements as VRNE
from .util import clean_filename


def os_join(*args):
    return os.path.join(*args)


class Uploader:
    def __init__(
        self,
        network: dict,
        p_name: str,
        skip_exists: bool,
        stringify: bool,
        p_path: str = _PROJECTS_PATH,
    ) -> None:
        self.network = network
        self.p_name = p_name  # Name of the project
        self.pf_path = p_path  # Path to the directory that contains all projects
        self.skip_exists = skip_exists  # boolean that indicates whether to skip existing project files or to update them
        self.strigify = (
            stringify  # boolean that indicates whether a network should be stringified
        )

    def makeProjectFolders(self) -> None:
        self.p_path = os_join(_PROJECTS_PATH, self.p_name)
        self.pfile_file = os_join(self.p_path, "pfile.json")
        self.names_file = os_join(self.p_path, "names.json")

        self.pfile = {}
        self.attr_list = {}
        self.pfile["name"] = self.p_name
        self.pfile["layouts"] = []
        self.pfile["layoutsRGB"] = []
        self.pfile["links"] = []
        self.pfile["linksRGB"] = []
        self.pfile["selections"] = []

        path = self.p_path

        os.makedirs(path, exist_ok=os.X_OK)
        os.makedirs(os_join(path, "layouts"), exist_ok=os.X_OK)
        os.makedirs(os_join(path, "layoutsl"), exist_ok=os.X_OK)
        os.makedirs(os_join(path, "layoutsRGB"), exist_ok=os.X_OK)
        os.makedirs(os_join(path, "links"), exist_ok=os.X_OK)
        os.makedirs(os_join(path, "linksRGB"), exist_ok=os.X_OK)

        with open(self.pfile_file, "w") as outfile:
            json.dump(self.pfile, outfile)

        with open(self.names_file, "w") as outfile:
            json.dump(self.attr_list, outfile)

        print("Successfully created directories in %s " % path)

    def loadProjectInfo(self) -> dict or str:
        self.folder = os_join(self.p_path)
        self.layoutfolder = os_join(self.folder, "layouts")
        self.layoutRGBfolder = os_join(self.folder, "layoutsRGB")
        self.linksRGBfolder = os_join(self.folder, "linksRGB")
        self.linkfolder = os_join(self.folder, "links")

        if os.path.exists(self.folder):

            layouts = [name for name in os.listdir(self.layoutfolder)]
            layoutsRGB = [name for name in os.listdir(self.layoutRGBfolder)]
            links = [name for name in os.listdir(self.linkfolder)]
            linksRGB = [name for name in os.listdir(self.linksRGBfolder)]

            return jsonify(
                layouts=layouts, layoutsRGB=layoutsRGB, links=links, linksRGB=linksRGB
            )
        else:
            return "no such project"

    @staticmethod
    def loadAnnotations(p_path: str) -> dict:
        """Return all annotations corresponding to a project name."""
        namefile = os_join(p_path, "names.json")
        f = open(namefile)
        data = json.load(f)
        return data

    @staticmethod
    def listProjects(projects_path: str = _PROJECTS_PATH) -> list:
        """Returns a list of all projects."""
        projects_path
        os.makedirs(projects_path, exist_ok=os.X_OK)
        sub_folders = [
            name
            for name in os.listdir(projects_path)
            if os.path.isdir(os_join(projects_path, name))
        ]
        # print(sub_folders)
        return sub_folders

    @staticmethod
    def extract_node_data(elem, layouts, attr_list, skip_attr):
        tex = []
        elem_lays = {lay[LT.name]: idx for idx, lay in enumerate(elem[NT.layouts])}
        for idx, layout in enumerate(layouts):
            tex.append([])
            coords = [0, 0, 0]  # x,y,z
            color = [0, 255, 255, 255]  # r,g,b,a
            attr_list = extract_attributes(attr_list, elem, skip_attr)

            if layout in elem_lays:
                l_idx = elem_lays[layout]
                lay = elem[NT.layouts][l_idx]
                position = lay[LT.position]

                if LT.color in lay:
                    if isinstance(lay[LT.color], list):
                        color = lay[LT.color]

                for d, _ in enumerate(position):
                    coords[d] = int(float(position[d]) * 65280)

            high = [value // 255 for value in coords]
            low = [value % 255 for value in coords]

            tex[idx].append(tuple(high))
            tex[idx].append(tuple(low))
            tex[idx].append(tuple(color))

        return tex

    @staticmethod
    def extract_link_data(elem, layouts):
        tex = None
        if ET.layouts in elem.keys():
            elem_lays = {lay[LT.name]: idx for idx, lay in enumerate(elem[ET.layouts])}
            start = elem[ET.start]
            end = elem[ET.end]
            sx = start % 128
            syl = start // 128 % 128
            syh = start // 16384

            ex = end % 128
            eyl = end // 128 % 128
            eyh = end // 16384
            tex = []
            for idx, layout in enumerate(layouts):
                color = [0, 100, 255, 255]
                tex.append([])
                if layout in elem_lays:
                    layout_idx = elem_lays[layout]
                    layout = elem[ET.layouts][layout_idx]
                    if LT.color in layout:
                        if isinstance(layout[LT.color], tuple):
                            color = layout[LT.color]
                else:
                    color = [0, 0, 0, 0]

                tex[idx].append((sx, syl, syh))
                tex[idx].append((ex, eyl, eyh))
                tex[idx].append(tuple(color))

        return tex

    def makeNodeTex(
        self,
        nodes,
        layouts=[LT._3d],
        skip_attr=["layouts"],
    ) -> str:
        """Generates Node textures from a dictionary of nodes."""
        n = len(nodes)  # Number of Nodes
        hight = 128 * (int(n / 16384) + 1)

        size = 128 * hight
        path = self.p_path

        l_tex = []
        l_img = []
        for l in layouts:
            l_tex.append(
                [[(0, 0, 0)] * size, [(0, 0, 0)] * size, [(0, 0, 0, 0)] * size]
            )
            l_img.append(
                [
                    Image.new("RGB", (128, hight)),
                    Image.new("RGB", (128, hight)),
                    Image.new("RGBA", (128, hight)),
                ]
            )

        for idx, elem in enumerate(nodes):
            tex = self.extract_node_data(elem, layouts, self.attr_list, skip_attr)
            for l, _ in enumerate(layouts):
                for d in range(3):
                    l_tex[l][d][idx] = tex[l][d]
        output = ""

        for l, layout in enumerate(layouts):
            for d in range(3):
                l_img[l][d].putdata(l_tex[l][d])
                # new_imgl.putdata(texl)
                # new_imgc.putdata(texc)

            pathXYZ = os_join(path, "layouts", f"{layout}XYZ.bmp")
            pathXYZl = os_join(path, "layoutsl", f"{layout}XYZl.bmp")
            pathRGB = os_join(path, "layoutsRGB", f"{layout}RGB.png")
            self.pfile["layouts"].append(f"{layout}XYZ")
            self.pfile["layoutsRGB"].append(f"{layout}RGB")

            if not self.skip_exists:
                l_img[l][0].save(pathXYZ)
                l_img[l][1].save(pathXYZl)
                l_img[l][2].save(pathRGB, "PNG")
                output += (
                    '<a style="color:green;">SUCCESS </a>'
                    + layout
                    + " Node Textures Created"
                )
            else:
                if os.path.exists(pathXYZ):
                    output += (
                        '<a style="color:red;">ERROR </a>'
                        + layout
                        + " Nodelist already in project"
                    )
                else:
                    l_img[l][0].save(pathXYZ)
                    l_img[l][1].save(pathXYZl)
                    l_img[l][2].save(pathRGB, "PNG")
                    output += (
                        '<a style="color:green;">SUCCESS </a>'
                        + layout
                        + " Node Textures Created"
                    )
        return output

    # TODO other name for variable filename. maybe Layout name
    def makeLinkTex(self, links: dict, nodes: dict, layouts: list) -> str:
        """Generate a Link texture from a dictionary of edges."""
        hight = 512
        path = self.p_path

        l_tex = []
        l_img = []

        for l in layouts:
            l_tex.append([[(0, 0, 0)] * 1024 * hight, [(0, 0, 0, 0)] * 512 * hight])
            l_img.append(
                [Image.new("RGB", (1024, hight)), Image.new("RGBA", (512, hight))]
            )
        # texl = [(0, 0, 0)] * 1024 * hight
        # texc = [(0, 0, 0, 0)] * 512 * hight
        # new_imgl = Image.new("RGB", (1024, hight))
        # new_imgc = Image.new("RGBA", (512, hight))

        l_idx = [0 for _ in layouts]
        for elem in links:
            tex = self.extract_link_data(elem, layouts)
            if tex is None:
                continue
            for l, layout in enumerate(layouts):
                if tex[l][2] is not None:
                    idx = l_idx[l]
                    if idx >= 262144:
                        continue
                    l_tex[l][0][idx * 2] = tex[l][0]  # texl[i * 2] = pixell1
                    l_tex[l][0][idx * 2 + 1] = tex[l][1]  # texl[i * 2 + 1] = pixell2
                    l_tex[l][1][idx] = tex[l][2]  # texc[i] = pixelc
                    l_idx[l] += 1

        output = ""
        for l, layout in enumerate(layouts):
            l_img[l][0].putdata(l_tex[l][0])  # new_imgl.putdata(texl)
            l_img[l][1].putdata(l_tex[l][1])  # new_imgc.putdata(texc)
            pathl = os_join(path, "links", f"{layout}XYZ.bmp")
            pathRGB = os_join(path, "linksRGB", f"{layout}RGB.png")
            self.pfile["links"].append(f"{layout}XYZ")
            self.pfile["linksRGB"].append(f"{layout}RGB")

            if not self.skip_exists:
                l_img[l][0].save(pathl, "PNG")
                l_img[l][1].save(pathRGB, "PNG")
                output += (
                    '<a style="color:green;">SUCCESS </a>'
                    + layout
                    + " Link Textures Created"
                )
            else:
                if os.path.exists(pathl):
                    output += (
                        '<a style="color:red;">ERROR </a>'
                        + layout
                        + " linklist already in project"
                    )
                else:
                    l_img[l][0].save(pathl, "PNG")
                    l_img[l][0].save(pathRGB, "PNG")
                    output += (
                        '<a style="color:green;">SUCCESS </a>'
                        + layout
                        + " Link Textures Created"
                    )

        return output

    @staticmethod
    def extract_desired_data(network, ingored_elements):
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
        return nodes_data, edges_data

    def stringify_project(self):
        """Changes the order of layouts in the pfile to start with a Cytoscape 2D network on the floor with all edges, than a new calculated 2D layout, and than the 3D layout with all edges after one another."""
        ev = EV.get_default_scheme().keys()
        ev_xyz = [f"{ev}XYZ" for ev in ev]
        ev_rgb = [f"{ev}RGB" for ev in ev]
        self.pfile[PT.links] = [ev_xyz[0], ev_xyz[0]] + ev_xyz
        self.pfile[PT.links_rgb] = [ev_rgb[0], ev_rgb[0]] + ev_rgb
        self.pfile[PT.layouts] = [
            f"{LT.cy_layout}XYZ",
            f"{LT.string_3d_no_z}XYZ",
            f"{LT.string_3d}XYZ",
        ]
        self.pfile[PT.layouts_rgb] = [
            f"{LT.cy_layout}RGB",
            f"{LT.string_3d_no_z}RGB",
            f"{LT.string_3d}RGB",
        ]
        for _ in ev:
            self.pfile[PT.layouts].append(self.pfile[PT.layouts][-1])
            self.pfile[PT.layouts_rgb].append(self.pfile[PT.layouts_rgb][-1])

        with open(self.pfile_file, "w") as json_file:
            json.dump(self.pfile, json_file)

    def upload_files(
        self,
        network: dict,
    ) -> str:
        """Generates textures and upload the needed network files. If created_2d_layout is True, it will create 2d layouts of the network one based on the cytoscape coordinates and one based on the new coordinated that come from the 3D layout without the z-coordinate.
        Furthermore, for each STRING evidence a edge texture with the respective color will be generated. If it is not a STRING network, only a single edge layout is created."""
        project = clean_filename(self.p_name)

        # Set up project directories
        prolist = self.listProjects(self.pf_path)

        if not self.skip_exists:
            self.makeProjectFolders()
        else:
            if project in prolist:
                print("project exists")
            else:
                # Make Folders
                self.makeProjectFolders()

        state = ""

        nodes = network[VRNE.nodes]
        links = network[VRNE.links]
        n_lay = network[VRNE.node_layouts]  # Node layouts
        l_lay = network[VRNE.link_layouts]

        with open(self.names_file, "r") as json_file:
            self.attr_list = json.load(json_file)

        with open(self.pfile_file, "r") as json_file:
            self.pfile = json.load(json_file)

        state += self.makeNodeTex(nodes, layouts=n_lay)

        state += self.makeLinkTex(links, nodes, l_lay)

        # update the projects file
        with open(self.pfile_file, "w") as json_file:
            json.dump(self.pfile, json_file)

        with open(self.names_file, "w") as json_file:
            json.dump(self.attr_list, json_file)

        global sessionData
        sessionData["proj"] = self.listProjects(self.pf_path)

        return state


def extract_attributes(attr_list, elem, skip_attr):
    if AT.names not in attr_list:
        attr_list["names"] = []
    name = ["NA"]

    if NT.stringdb_canoncial_name in elem.keys():
        uniprod = elem[NT.stringdb_canoncial_name]
        name = [
            uniprod,  # identifier
            "None",  # Attribute
            uniprod,  # Annotation
            50,  # Additional
        ]
        if NT.stringdb_sequence in elem.keys():
            name[-1] = elem[NT.stringdb_sequence]
    elif NT.name in elem.keys():
        gene_name = elem[NT.name]
        name = [f"GENENAME={gene_name}"]

    attr_list["names"].append(name)
    attributes = [k for k in elem.keys() if k not in skip_attr]
    for attr in attributes:
        if not attr in attr_list:
            attr_list[attr] = []
        attr_list[attr].append([elem[attr]])
    return attr_list


if __name__ == "__main__":
    _FILE_PATH = os.path.abspath(f"{__file__}/../../")
    _PROJECTS_PATH = f"{_FILE_PATH}/static/projects"
    sessionData["proj"] = Uploader.listProjects(_PROJECTS_PATH)
    print(sessionData["proj"])

# def create_2d_layouts(self,nodes,layout
# ):
#     # Create 2D Layout of Cytoscape coordinates node texture
#     filename = f"{self.project}_{layout}"
#     output =self.makeNodeTex(nodes,layout)
#     self.pfile["layouts"].append(f"{filename}XYZ")
#     self.pfile["layoutsRGB"].append(f"{filename}RGB")
#     self.pfile["links"].append(f"anyXYZ")
#     self.pfile["linksRGB"].append(f"anyRGB")

#     return output

# def create_3d_eviedence_layout(self,linksevidences):
#     # For each evidence type, create a texture and upload it
#     for evidence in evidences:
#         edges = edges_data.copy()
#         if not evidence == "any":
#             edges = {
#                 edge: data for edge, data in edges.items() if evidence in data.keys()
#             }
#         # Skip This evidence if there are not edges for this evidence
#         if len(edges) == 0:
#             continue

#         # Color each link with the color of the evidence
#         for edge in edges:
#             if evidence == "any":
#                 color = evidences[evidence]
#                 # TODO extract the alpha value with the highest score.
#             else:
#                 color = evidences[evidence][:2] + (
#                     int(edges[edge][evidence] * 255),
#                 )  # Alpha scales with score
#             edges[edge]["color"] = color

#         # Add node layout to pflie for this link layout
#         pfile["layouts"].append(f"{filename}XYZ")
#         pfile["layoutsRGB"].append(f"{filename}RGB")

#         # Add link layout to pfile
#         pfile["links"].append(f"{evidence}XYZ")
#         pfile["linksRGB"].append(f"{evidence}RGB")

#         # Generate link texture
#         state += f"{state}<br>{makeLinkTex(project,evidence,edges,nodes_data.keys(),projects_path,skip_exists)}"
