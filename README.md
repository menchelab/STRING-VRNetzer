# **STRING-VRNetzer**
Access protein-protein association networks from STRING DB in VRNetzer

### Miro Board
https://miro.com/app/board/uXjVOtKWqXI=/?share_link_id=552918253097
## Content
[Fetch STRING Networks](#Fetch-STRING-Networks)<br>
[Cytoscape APP](#Cytoscape-App)<br>
[**Dependencies**](#Dependencies)<br>

## **Fetch STRING Networks**

TODO

## **Cytoscape App**

The Cytoscape app is located here:<br>
https://github.com/menchelab/STRING-VRNetzer/blob/main/cytoscapeApp/VRNetzerApp/target/VRNetzerApp-1.0.0.jar

### **Installation of the App**

To install it, you can use the App Manger in Cytoscape:<br>
Apps -> App Manger -> Install from File... -> select the "VRNetzerApp-x.x.x.jar" file.

### **Usage of the App**

1. Select a network you would like to export.
2. Export the selected network as an "VRNetz" via:<br>
    a) Apps -> VRNetzer -> Export network as VRNetz<br>
    or <br>
    b) File -> Export -> Export network as VRNetz
3. Select the location where to save the network, as well as a name in the propted window.

You network is now exported as an VRNetz which can be used in the [VRNetzer](https://github.com/menchelab/VRNetzer) to present your network as a 3D network.
## **Dependencies**
python==3.9
networkx==
[Cytoscape - StringApp](https://apps.cytoscape.org/apps/stringapp)
## **Software**
[VRNetzer](https://github.com/menchelab/VRNetzer)<br>
[Cytoscape v3.8. ++](https://cytoscape.org/)<br>

## **License**
TODO