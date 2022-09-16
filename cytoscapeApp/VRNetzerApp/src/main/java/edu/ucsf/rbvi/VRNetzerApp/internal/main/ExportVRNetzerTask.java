package edu.ucsf.rbvi.VRNetzerApp.internal.main;

import java.awt.Color;
import java.io.File;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.cytoscape.io.write.CyWriter;
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
import org.cytoscape.work.Tunable;
import org.javatuples.Triplet;
import org.json.simple.JSONObject;

// https://github.com/cytoscape/cx/tree/master/src/main/java/org/cytoscape/io/internal!!!!!!!!!!!
import edu.ucsf.rbvi.VRNetzerApp.internal.util.ConstructJson;


public class ExportVRNetzerTask extends AbstractTask implements CyWriter {

	final CyServiceRegistrar registrar;
	private CyNetwork network;
	//TODO Change that the default name of the file is "untitled"
	@Tunable(description = "Save network as <fileName>.VRNetz", params = "input=false", 
	         tooltip="<html>Note: for convenience spaces are replaced by underscores.</html>",gravity = 1.0)
	public File fileName = null;
//	@Tunable(description = "Select namespace to export.", params = "input=false",gravity = 2.0)
//	public String namespace = null; // Not so sure about that one.
	
	private CyNetworkView netView;
	final private List<String> skip_columns = Arrays.asList("stringdb::STRING style","selected","stringdb_namespace","stringdb_enhancedLabel Passthrough");

	public ExportVRNetzerTask(CyServiceRegistrar registrar, CyNetwork network) {
		this.registrar = registrar;
		this.network = network;
	}

	@Override
	public void run(TaskMonitor monitor) throws Exception {
		monitor.setTitle("Export network as VRNetz");
		// Get current network
		
        Collection<CyNetworkView> views = registrar.getService(CyNetworkViewManager.class).getNetworkViews(network);
        if (views.isEmpty()){
		monitor.setTitle("Error: No network view!");
    	   monitor.showMessage(TaskMonitor.Level.ERROR,"You first have to create a network view!");
    	   throw new RuntimeException("You first have to create a network view!");
        }
        // Get NetView
        for (CyNetworkView view: views) {
            if (view.getRendererId().equals("org.cytoscape.ding")) {
            	netView = view;
                break;
            }
        } 
		// Get all nodes/edges and their Data from the corresponding table
        long startTime = System.currentTimeMillis();
		CyTable nodes = network.getTable(CyNode.class, CyNetwork.LOCAL_ATTRS);
        long stopTime = System.currentTimeMillis();
        long totalTime = stopTime - startTime;
        double totalTimeInSeconds = (double) stopTime-startTime / 1_000_000_000;
        
		monitor.showMessage(TaskMonitor.Level.INFO, "Extracting node data from table took:"+String.valueOf(totalTime));
        startTime = System.currentTimeMillis();
	    CyTable edges = network.getTable(CyEdge.class, CyNetwork.LOCAL_ATTRS);
        stopTime = System.currentTimeMillis();
        totalTime = stopTime - startTime;
        totalTimeInSeconds = (double) stopTime-startTime / 1_000_000_000;
		monitor.showMessage(TaskMonitor.Level.INFO, "Extracting edge data from table took:"+String.valueOf(totalTime));


        startTime = System.currentTimeMillis();
		Map<String,Object>nodesData = getData(nodes,CyNode.class);
        stopTime = System.currentTimeMillis();
        totalTime = stopTime - startTime;
        totalTimeInSeconds = (double) stopTime-startTime / 1_000_000_000;
		monitor.showMessage(TaskMonitor.Level.INFO, "Generating node Map took:"+String.valueOf(totalTime));

        startTime = System.currentTimeMillis();
		Map<String,Object>edgesData = getData(edges,CyEdge.class);
        stopTime = System.currentTimeMillis();
        totalTime = stopTime - startTime;
        totalTimeInSeconds = (double) stopTime-startTime / 1_000_000_000;
		monitor.showMessage(TaskMonitor.Level.INFO, "Generating edge Map took:"+String.valueOf(totalTime));
		
		if (fileName != null) {
			// Set Names
			String _fileName = fileName.getAbsolutePath();
			_fileName = _fileName.replace(' ','_');
			if (!_fileName.endsWith(".VRNetz"))
				_fileName += ".VRNetz";
			// Write data to json
			ConstructJson exportFile = new ConstructJson(_fileName);
			JSONObject nodesJson = exportFile.generateObject("nodes", nodesData);
			JSONObject edgesJson = exportFile.generateObject("edges", edgesData);
			JSONObject networkJson = new JSONObject();
			networkJson.put("nodes", nodesJson);
			networkJson.put("edges", edgesJson);
			
			monitor.showMessage(TaskMonitor.Level.INFO, "Writing data of '"+network.toString()+"'");
	        startTime = System.nanoTime();
			exportFile.writeObject(networkJson); // TODO Improve the writing performance, if we need more nodes to be exported!
	        stopTime = System.nanoTime();
	        totalTime = stopTime - startTime;
	        totalTimeInSeconds = (double) stopTime-startTime / 1_000_000_000;
			monitor.showMessage(TaskMonitor.Level.INFO, "Writing file took:"+String.valueOf(totalTimeInSeconds));
			
			monitor.setStatusMessage("Exported network to '"+_fileName+"'");
			
		}
	}
	public Map<String,Object> getStyle(CyNode node){
		 /**
		 * Extracts properties from the node style.
		 * <p>
		 * Some more description.
		 * <p>
		 * And even more explanations to follow in consecutive
		 * paragraphs separated by HTML paragraph breaks.
		 *
		 * @param  CyNode          (3)
		 * @return A HashMap containing the property as key and the value data as Object
		 */
		Map<String,Object> node_prop = new HashMap<>();
		View<CyNode> view = netView.getNodeView(node);
		String node_label = view.getVisualProperty(BasicVisualLexicon.NODE_LABEL);
		Double x = view.getVisualProperty(BasicVisualLexicon.NODE_X_LOCATION);
		Double y = view.getVisualProperty(BasicVisualLexicon.NODE_Y_LOCATION);
		Double z = view.getVisualProperty(BasicVisualLexicon.NODE_Z_LOCATION);
		Double node_size = view.getVisualProperty(BasicVisualLexicon.NODE_SIZE);
		Color node_color = (Color) view.getVisualProperty(BasicVisualLexicon.NODE_FILL_COLOR);
		Triplet<Integer, Integer, Integer> rgb = new Triplet<Integer, Integer, Integer>(node_color.getRed(),
				node_color.getGreen(), node_color.getBlue());
		Triplet<Double, Double, Double> xyz = new Triplet<Double, Double, Double>(x,y,z);
		node_prop.put("node_label", node_label);
		node_prop.put("node_Cytoscape_pos", xyz);
		node_prop.put("node_color", rgb);
		node_prop.put("node_size", node_size);
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
			 
			 // Generate a new HashMap for Data of node/edge
			 Map<String,Object> data = new HashMap<>();
			 
			 // For nodes, extract the color from the style
			 if (type == CyNode.class) {
				 CyNode node =  network.getNode(suid);
				 data.putAll(getStyle(node));
			 }
			 // For edges, extract source and sink and add it to the map
			 else if (type == CyEdge.class){
				 CyEdge edge =  network.getEdge(suid);
				 data.put("source",   edge.getSource().getSUID());
				 data.put("sink",  edge.getTarget().getSUID());
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
	@ProvidesTitle
	public String getTitle() {
		return "Export Network as VRNetz";
	}
}
