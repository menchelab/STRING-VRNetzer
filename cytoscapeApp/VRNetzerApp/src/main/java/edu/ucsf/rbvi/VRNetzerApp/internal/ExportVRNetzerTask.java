package edu.ucsf.rbvi.VRNetzerApp.internal;

import org.cytoscape.model.CyNetworkManager;
import org.cytoscape.model.CyColumn;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyTable;
import org.cytoscape.model.CyIdentifiable;
import org.cytoscape.model.CyRow;
import org.cytoscape.model.CyNode;
import org.cytoscape.model.CyEdge;
import org.cytoscape.view.model.CyNetworkViewManager;
import org.cytoscape.view.model.CyNetworkView;

import org.cytoscape.view.model.View;
import org.cytoscape.view.presentation.property.BasicVisualLexicon;
import org.cytoscape.view.layout.LayoutNode;

import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.task.write.ExportTableTaskFactory;

import org.cytoscape.work.AbstractTask;
import org.cytoscape.work.ProvidesTitle;
import org.cytoscape.work.TaskIterator;
import org.cytoscape.work.TaskMonitor;
import org.cytoscape.work.Tunable;

import java.awt.Paint;
import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

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

	public void run(TaskMonitor monitor) {
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
		printMap(nodesData);
//		printMap(edgesData);
//		VisualStyle style = mappingManager.getCurrentVisualStyle();
//		if (style == null)
//			style = styleFactory.createVisualStyle("default");
//		System.out.println("My network is: " + network.toString());
//		System.out.println("My style is: "+ style.toString());
//		monitor.showMessage(TaskMonitor.Level.INFO,
//				"Exporting network "+ network.toString() +
//				"with style " + style.toString() );
//		ExportTableTaskFactory exportTF = registrar.getService(ExportTableTaskFactory.class);
//		if (network != null && fileName != null) {
//			File file = fileName;
//			monitor.showMessage(TaskMonitor.Level.INFO,
//					"export network " + network + "with style "+style+" to " + file.getAbsolutePath());
//		}
	}
	public void printMap(Map<String,Object> map) {
	for (Map.Entry<String, Object> entry : map.entrySet()) {
	    String thisEntry = entry.getKey();
	    Map<String,Object> data = (Map<String,Object>) entry.getValue();
	    String k = "";
		String v= "";
		System.out.println(thisEntry);
	    for (Map.Entry<String, Object> dataPoint : data.entrySet()) {
	    	k = dataPoint.getKey();
	    	v = dataPoint.getValue().toString();
		    System.out.printf("\t%s = %s\n", k, v);
	    }
	    System.out.println("");
	}
	}
	@ProvidesTitle
	public String getTitle() {
		return "Export Network as VRNetz";
	}
	public String getStyle(CyNode node){
			View<CyNode> view = netView.getNodeView(node);
//			String node_label = view.getVisualProperty(BasicVisualLexicon.NODE_LABEL);
//			Double node_size = view.getVisualProperty(BasicVisualLexicon.NODE_SIZE);
			Paint node_color = view.getVisualProperty(BasicVisualLexicon.NODE_FILL_COLOR);
			return node_color.toString();
		}
	
	@SuppressWarnings("unchecked")
	public Map<String,Object> getData(CyTable table,List<?> identifier){
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
		Collection<CyColumn> columns = table.getColumns();
		Object[] columnsArray = columns.toArray();
		List<CyRow> rows = table.getAllRows();
		Map<String,Object> identMap = new HashMap<>();
		for (int i=0; i<rows.size(); i++) {
			 CyRow row = rows.get(i);
			 CyIdentifiable suid =  (CyIdentifiable) identifier.get(i);
			 String suid_string = (String) suid.getSUID().toString();
			Map<String,Object> data = new HashMap<>();
			 if (nodes) {
				 String node_color = getStyle((CyNode) suid);
				 data.put("color", node_color);
			 }
			 for(int j=0; j< columnsArray.length;j++) {
				 String key = columnsArray[j].toString();
				 Object value = row.getRaw(columnsArray[j].toString());
				 boolean skip = false;
				 for(String col: skip_columns) {
					 if (key.equals(col)) {
						 skip = true;
						 break;
					 }
				 }
				 if (value != null & !skip) {
					 data.put(key, value);
				 }
			 }
			 identMap.put(suid_string,data);
		}
		return identMap;
	}

}
