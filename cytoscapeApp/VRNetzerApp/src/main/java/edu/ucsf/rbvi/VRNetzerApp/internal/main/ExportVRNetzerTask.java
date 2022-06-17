package edu.ucsf.rbvi.VRNetzerApp.internal.main;

import java.awt.Color;
import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.lang.Long;

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
//import org.cytoscape.io.internal.cx_writer.*;

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
		CyTable nodes = network.getTable(CyNode.class, CyNetwork.LOCAL_ATTRS);
	    CyTable edges = network.getTable(CyEdge.class, CyNetwork.LOCAL_ATTRS);
	    try {
		    edges.createColumn("source", Long.class,true);
		    edges.createColumn("sink", Long.class,true);
	    } catch (IllegalArgumentException e){
	    	//
	    }
		Map<String,Object>nodesData = getData(nodes,CyNode.class);
		Map<String,Object>edgesData = getData(edges,CyEdge.class);
		String filename = "/Users/till/Documents/UNI/Master_Bioinformatik-Universität_Wien/3.Semester/Masterthesis/STRING-VRNetzer/static/networks/test.json";
		ConstructJson exportFile = new ConstructJson(filename);
		JSONObject nodesJson = exportFile.generateObject("nodes", nodesData);
		JSONObject edgesJson = exportFile.generateObject("edges", edgesData);
		// TODO SUIDs are inconsistent!
		JSONObject networkJson = new JSONObject();
		networkJson.put("nodes", nodesJson);
		networkJson.put("edges", edgesJson);
		exportFile.writeObject(networkJson);
	}
	@ProvidesTitle
	public String getTitle() {
		return "Export Network as VRNetz";
	}
	public Map<String,Object> getStyle(CyNode node){
			Map<String,Object> node_prop = new HashMap<>();
			View<CyNode> view = netView.getNodeView(node);
			String node_label = view.getVisualProperty(BasicVisualLexicon.NODE_LABEL);
			Double x = view.getVisualProperty(BasicVisualLexicon.NODE_X_LOCATION);
			Double y = view.getVisualProperty(BasicVisualLexicon.NODE_Y_LOCATION);
			Double z = view.getVisualProperty(BasicVisualLexicon.NODE_Z_LOCATION);
//			Double node_size = view.getVisualProperty(BasicVisualLexicon.NODE_SIZE);
			Color node_color = (Color) view.getVisualProperty(BasicVisualLexicon.NODE_FILL_COLOR);
			Triplet<Integer, Integer, Integer> rgb = new Triplet<Integer, Integer, Integer>(node_color.getRed(),
					node_color.getGreen(), node_color.getBlue());
			Triplet<Double, Double, Double> xyz = new Triplet<Double, Double, Double>(x,y,z);
			node_prop.put("label", node_label);
			node_prop.put("2d_pos", xyz);
			node_prop.put("color", rgb);
			return  node_prop;
		}
	
	@SuppressWarnings("unchecked")
	public Map<String,Object> getData(CyTable table, Class<? extends CyIdentifiable> type){
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
		if (!(type == CyNode.class) & !(type == CyEdge.class))
			return new HashMap<>();
		
		// get all Columns in the corresponding table
		Collection<CyColumn> columns = table.getColumns();
		Object[] columnsArray = columns.toArray();
		
		// extract all rows
		List<CyRow> rows = table.getAllRows();
		Map<String,Object> identMap = new HashMap<>();
		
		for (int i=0; i<rows.size(); i++) {
			 CyRow row = rows.get(i);
			 Long suid = row.get("SUID", Long.class);
			 // Get the SUID for corresponding Line (i.e. SUID of node/edge)
			 // GET CyNode from Network based on SUID!
			 // Generate a new HashMap for Data of node/edge
			 Map<String,Object> data = new HashMap<>();
			 // For nodes, extract the color from the style
			 if (type == CyNode.class) {
				 CyNode node =  network.getNode(suid);
				 data.putAll(getStyle(node));
			 }
			 else if (type == CyEdge.class){
				 CyEdge edge =  network.getEdge(suid);
				 row.set("source",   edge.getSource().getSUID());
				 row.set("sink",  edge.getTarget().getSUID());
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
			 identMap.put(suid.toString(),data);
		}
		return identMap;
	}

}
