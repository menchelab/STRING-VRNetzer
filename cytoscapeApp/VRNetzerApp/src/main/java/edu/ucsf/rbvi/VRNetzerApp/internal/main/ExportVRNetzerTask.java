package edu.ucsf.rbvi.VRNetzerApp.internal.main;

import java.awt.Color;
import java.io.File;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.cytoscape.model.CyColumn;
import org.cytoscape.model.CyEdge;
import org.cytoscape.model.CyIdentifiable;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyNode;
import org.cytoscape.model.CyRow;
import org.cytoscape.model.CyTable;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.view.model.CyNetworkViewManager;
import org.cytoscape.view.model.View;
import org.cytoscape.view.presentation.property.BasicVisualLexicon;
import org.cytoscape.work.AbstractTask;
import org.cytoscape.work.ProvidesTitle;
import org.cytoscape.work.TaskMonitor;
import org.javatuples.Triplet;
import org.json.simple.JSONObject;

// https://github.com/cytoscape/cx/tree/master/src/main/java/org/cytoscape/io/internal!!!!!!!!!!!
import edu.ucsf.rbvi.VRNetzerApp.internal.util.ConstructJson;
// Export Table
// ExportEnrichmentTable
// Call already implemented Task
// MCLClusterTask

public class ExportVRNetzerTask extends AbstractTask {

	final CyServiceRegistrar registrar;
	private CyNetwork network;
	
//	@Tunable(description = "Save Network as", params = "input=false", 
//	         tooltip="<html>Note: for convenience spaces are replaced by underscores.</html>", gravity = 2.0)
	public File fileName = null;
	private CyNetworkView netView;
	final private List<String> skip_columns = Arrays.asList("stringdb::STRING style","selected");
	
//	private final VisualStyle style;

	public ExportVRNetzerTask(CyServiceRegistrar registrar, CyNetwork network) {
		this.network = network;
		this.registrar = registrar;
	}

	public void run(TaskMonitor monitor) throws Exception {
		monitor.setTitle("Export network as VRNetz");
		// Get current network

        Collection<CyNetworkView> views = registrar.getService(CyNetworkViewManager.class).getNetworkViews(network);
        // Get NetView
        for (CyNetworkView view: views) {
            if (view.getRendererId().equals("org.cytoscape.ding")) {
            	netView = view;
                break;
            }
        } 
		// Get all nodes/edges and their Data from the corresponding table
		CyTable nodes = network.getDefaultNodeTable();
	    CyTable edges = network.getDefaultEdgeTable();
	    List<CyNode> nodesSuids = network.getNodeList();
	    List<CyEdge> edgesSuids = network.getEdgeList();
		Map<String,Object>nodesData = getData(nodes,nodesSuids);
		Map<String,Object>edgesData = getData(edges,edgesSuids);
		String filename = "/Users/till/Documents/UNI/Master_Bioinformatik-Universität_Wien/3.Semester/Masterthesis/STRING-VRNetzer/static/networks/test.json";
		ConstructJson exportFile = new ConstructJson(filename);
		JSONObject nodesJson = exportFile.generateObject("nodes", nodesData);
		JSONObject edgesJson = exportFile.generateObject("edges", edgesData);
		// TODO GET SOURCE AND SINK FOR EDGE!
		JSONObject networkJson = new JSONObject();
		networkJson.put("nodes", nodesJson);
		networkJson.put("edges", edgesJson);
		exportFile.writeObject(networkJson);
	}
	@ProvidesTitle
	public String getTitle() {
		return "Export Network as VRNetz";
	}
	public Triplet<Integer, Integer, Integer> getStyle(CyNode node){
			View<CyNode> view = netView.getNodeView(node);
//			String node_label = view.getVisualProperty(BasicVisualLexicon.NODE_LABEL);
//			Double node_size = view.getVisualProperty(BasicVisualLexicon.NODE_SIZE);
			Color node_color = (Color) view.getVisualProperty(BasicVisualLexicon.NODE_FILL_COLOR);
			return new Triplet<Integer, Integer, Integer>(node_color.getRed(), node_color.getGreen(), node_color.getBlue()); ;
		}
	
	@SuppressWarnings("unchecked")
	public Map<String,Object> getData(CyTable table,List<?> identifier){
		 /**
		 * Extracts Data from CyTable (Nodes/Edges)                          (1)
		 * <p>
		 * Some more description.
		 * <p>
		 * And even more explanations to follow in consecutive
		 * paragraphs separated by HTML paragraph breaks.
		 *
		 * @param  CytTable          (3)
		 * @return A HashMap containing the SUID as key and the node/edge data as another HashMap
		 */
		
		// Define the type of the Elements in the given List.
		boolean nodes = false;
		if (identifier.get(0) instanceof CyEdge) {
			identifier = (List<CyEdge>) identifier;
		}else if (identifier.get(0) instanceof CyNode){
			identifier = (List<CyNode>) identifier;
			nodes = true;
		}else {
			identifier = (List<CyIdentifiable>) identifier;
			return new HashMap<>();
		}
		
		// get all Columns in the corresponding table
		Collection<CyColumn> columns = table.getColumns();
		Object[] columnsArray = columns.toArray();
		
		// extract all rows
		List<CyRow> rows = table.getAllRows();
		Map<String,Object> identMap = new HashMap<>();
		
		for (int i=0; i<rows.size(); i++) {
			 CyRow row = rows.get(i);
			 // Get the SUID for corresponding Line (i.e. SUID of node/edge)
			 CyIdentifiable suid =  (CyIdentifiable) identifier.get(i);
			 String suid_string = (String) suid.getSUID().toString();
			 
			 // Generate a new HashMap for Data of node/edge
			 Map<String,Object> data = new HashMap<>();
			 
			 // For nodes, extract the color from the style
			 if (nodes) {
				 Triplet<Integer, Integer, Integer> node_color = getStyle((CyNode) suid);
				 data.put("color", node_color);
			 }
			 // iterate through all columns and save data in the HashMap
			 for(int j=0; j< columnsArray.length;j++) {
				 String key = columnsArray[j].toString(); // Name of the Column
				 Object value = row.getRaw(columnsArray[j].toString()); // Value of the Column
				 boolean skip = false;
				 for(String col: skip_columns) {
					 if (key.equals(col)) {
						 skip = true;
						 break;
					 }
				 }
				 if (value != null & !skip) {
					 data.put(key.replace("::", "_"), value); // Remove weird :: characters from column names
				 }
			 }
			 identMap.put(suid_string,data);
		}
		return identMap;
	}

}
