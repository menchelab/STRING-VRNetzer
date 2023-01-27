package univie.menchelab.VRNetzerApp.internal.util;

import java.awt.Color;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.cytoscape.model.CyColumn;
import org.cytoscape.model.CyEdge;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyNode;
import org.cytoscape.model.CyRow;
import org.cytoscape.model.CyTable;
import org.cytoscape.model.CyTableManager;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.view.model.CyNetworkViewManager;
import org.cytoscape.view.model.View;
import org.cytoscape.view.presentation.property.BasicVisualLexicon;
import org.cytoscape.work.TaskMonitor;
import org.javatuples.Triplet;
import org.json.simple.JSONObject;


public class ConstructJson {
	private CyServiceRegistrar registrar;
	private TaskMonitor monitor;
	private CyNetwork network;
	private CyNetworkView netView;
	private ArrayList<String> layouts = new ArrayList<String>();
	private List<String> skipNodeColumns = new ArrayList<String>();
	private List<String> skipEdgeColumns = new ArrayList<String>();
	private Utility util = new Utility();

	public ConstructJson(CyServiceRegistrar registrar, TaskMonitor monitor, CyNetwork network,
			CyNetworkView netView, List<String> skipNodeColumns, List<String> skipEdgeColumns) {
		this.registrar = registrar;
		this.monitor = monitor;
		this.network = network;
		this.netView = netView;
		this.skipNodeColumns = skipNodeColumns;
		this.skipEdgeColumns = skipEdgeColumns;

	};

	@SuppressWarnings("unchecked")
	public JSONObject generateObject(String header, List<HashMap<String, Object>> data) {
		JSONObject objectToWrite = new JSONObject();
		objectToWrite.put(header, data);
		// objectToWrite.put("data_type", header); //Not needed and causes trouble
		// objectToWrite.put("amount", data.size()); //Not needed and causes trouble
		return objectToWrite;
	};

	public void validate() {
		Timer validationTimer = new Timer("Validating input.", monitor, TaskMonitor.Level.INFO);
		validationTimer.start();
		monitor.setTitle("Export network as VRNetz");
		// Get current network

		if (network == null) {
			monitor.showMessage(TaskMonitor.Level.WARN, "No network to export");
			throw new RuntimeException("No network to export!");
		}

		if (netView == null) {
			Collection<CyNetworkView> views =
					registrar.getService(CyNetworkViewManager.class).getNetworkViews(network);
			if (views.isEmpty()) {
				monitor.setTitle("Error: No network view!");
				monitor.showMessage(TaskMonitor.Level.ERROR,
						"You first have to create a network view!");
				throw new RuntimeException("You first have to create a network view!");
			}
		}
		validationTimer.stop();
	}

	@SuppressWarnings("unchecked")
	public JSONObject constructOutput() {
		Collection<CyNetworkView> views =
				registrar.getService(CyNetworkViewManager.class).getNetworkViews(network);
		// Get NetView
		for (CyNetworkView view : views) {
			if (view.getRendererId().equals("org.cytoscape.ding")) {
				netView = view;
				break;
			}
		}
		JSONObject networkJson = new JSONObject();
		CyTableManager tableManager = registrar.getService(CyTableManager.class);
		Set<CyTable> tables = tableManager.getAllTables(true);
		HashMap<Integer, Integer> suidOnId = new HashMap<Integer, Integer>();
		CyTable edges = null;
		// CyTableFactory tableFactory = registrar.getService(CyTableFactory.class);
		// List<CyTable> enrichmentTable = new ArrayList<CyTable>();
		String tableTitle = "";
		for (CyTable table : tables) {
			tableTitle = table.getTitle();
			if (tableTitle.contains("STRING Enrichment") && !(tableTitle.contains("PMID"))) {

				networkJson.put("enrichment", getEnrichmentData(table));

			} else if (table.getTitle().contains("PMID")) {

				networkJson.put("publications", getEnrichmentData(table));
			}
		} ;
		HashMap<String, Object> networkData =
				getNetworkData(network.getTable(CyNetwork.class, CyNetwork.LOCAL_ATTRS));
		networkJson.put("network", networkData);
		Object[] output = getNodeData(network.getTable(CyNode.class, CyNetwork.LOCAL_ATTRS));
		networkJson.put("nodes", (List<HashMap<String, Object>>) output[0]);
		suidOnId = (HashMap<Integer, Integer>) output[1];

		networkJson.put("links",
				getEdgeData(network.getTable(CyEdge.class, CyNetwork.LOCAL_ATTRS), suidOnId));


		// Write data to json
		layouts.add("cy");

		networkJson.put("layouts", layouts);
		return networkJson;
	}

	public Map<String, Object> getStyle(CyNode node) {
		/**
		 * Extracts properties from the node style.
		 * <p>
		 * Some more description.
		 * <p>
		 * And even more explanations to follow in consecutive paragraphs separated by HTML
		 * paragraph breaks.
		 *
		 * @param CyNode (3)
		 * @return A HashMap containing the property as key and the value data as Object
		 */
		Map<String, Object> node_prop = new HashMap<>();
		View<CyNode> view = netView.getNodeView(node);
		// System.out.println(view.getVisualProperty(BasicVisualLexicon.);
		String node_label = view.getVisualProperty(BasicVisualLexicon.NODE_LABEL);
		Double x = view.getVisualProperty(BasicVisualLexicon.NODE_X_LOCATION);
		Double y = view.getVisualProperty(BasicVisualLexicon.NODE_Y_LOCATION);
		Double z = view.getVisualProperty(BasicVisualLexicon.NODE_Z_LOCATION);
		Double node_size = view.getVisualProperty(BasicVisualLexicon.NODE_SIZE);
		Color node_color = (Color) view.getVisualProperty(BasicVisualLexicon.NODE_FILL_COLOR);
		Triplet<Integer, Integer, Integer> rgb = new Triplet<Integer, Integer, Integer>(
				node_color.getRed(), node_color.getGreen(), node_color.getBlue());
		Triplet<Double, Double, Double> xyz = new Triplet<Double, Double, Double>(x, y, z);

		node_prop.put("n", node_label); // set node name


		HashMap<String, Object> cytoscape_layout = new HashMap<String, Object>();
		cytoscape_layout.put("p", xyz); // set node Cytoscape position
		cytoscape_layout.put("c", rgb); // set node color
		cytoscape_layout.put("s", node_size); // set node size
		cytoscape_layout.put("n", "cy"); // set node size

		List<HashMap<String, Object>> layouts = new ArrayList<HashMap<String, Object>>();
		layouts.add(cytoscape_layout);
		node_prop.put("layouts", layouts);

		return node_prop;
	}

	public List<HashMap<String, Object>> getEnrichmentData(CyTable table) {
		List<HashMap<String, Object>> mapList = new ArrayList<HashMap<String, Object>>();
		List<CyRow> rows = table.getAllRows();
		Collection<CyColumn> columns = table.getColumns();
		Object[] columnsArray = columns.toArray();

		List<String> skip = Arrays.asList("nodes.SUID", "network.SUID");
		// System.out.println(rows.size());
		for (int i = 0; i < rows.size(); i++) {
			HashMap<String, Object> data = new HashMap<>();
			CyRow row = rows.get(i);
			data = util.writeData(data, columnsArray, row, skip);
			mapList.add(data);
		}
		return (List<HashMap<String, Object>>) mapList;

	}

	@SuppressWarnings("unchecked")
	public List<HashMap<String, Object>> getEdgeData(CyTable table,
			HashMap<Integer, Integer> suidOnId) {
		// For edges, extract source and sink and add it to the map
		Collection<CyColumn> columns = table.getColumns();
		Object[] columnsArray = columns.toArray();

		// extract all rows
		List<CyRow> rows = table.getAllRows();
		List<HashMap<String, Object>> mapList = new ArrayList<HashMap<String, Object>>();


		for (int i = 0; i < rows.size(); i++) {
			CyRow row = rows.get(i);
			Long suid = row.get("SUID", Long.class);
			// Get the SUID for corresponding Line (i.e. SUID of node/edge)

			// Generate a new HashMap for Data of node/edge
			HashMap<String, Object> data = new HashMap<>();


			// For nodes, extract the color from the style
			CyEdge edge = network.getEdge(suid);
			if (edge == null) {
				continue;
			}
			data.put("id", i);
			Integer s_suid = edge.getSource().getSUID().intValue();
			Integer e_suid = edge.getTarget().getSUID().intValue();
			data.put("s_suid", s_suid); // write start
			data.put("e_suid", e_suid); // write end

			Integer s_id = suidOnId.get(s_suid);
			Integer e_id = suidOnId.get(e_suid);

			data.put("s", s_id); // write start
			data.put("e", e_id); // write end

			data = util.writeData(data, columnsArray, row, skipEdgeColumns);
			mapList.add(data);
		}
		return (List<HashMap<String, Object>>) mapList;
	}

	public HashMap<String, Object> getNetworkData(CyTable table) {
		Collection<CyColumn> cols = table.getColumns();
		HashMap<String, Object> data = new HashMap<>();
		CyRow row = table.getAllRows().get(0);
		for (CyColumn col : table.getColumns()) {
			String colName = col.getName();
			if (colName.equals("analyzedNodes.SUID"))
				continue;
			data.put(col.getName(), row.getRaw(col.getName()));
		} ;
		return data;
	};

	@SuppressWarnings("unchecked")
	public Object[] getNodeData(CyTable table) {
		// public List<HashMap<String, Object>> getData(CyTable table, Class<? extends
		// CyIdentifiable> type){
		/**
		 * Extracts Data from CyTable (Nodes/Edges) (1)
		 * <p>
		 * Some more description.
		 * <p>
		 * And even more explanations to follow in consecutive paragraphs separated by HTML
		 * paragraph breaks.
		 *
		 * @param CytTable (3)
		 * @return A HashMap containing the SUID as key and the node/edge data as another HashMap
		 */

		// Define the type of the Elements in the given List.
		// if (!(type == CyNode.class) & !(type == CyEdge.class))
		// return new ArrayList<HashMap<String, Object>>();

		// get all Columns in the corresponding table
		Collection<CyColumn> columns = table.getColumns();
		Object[] columnsArray = columns.toArray();
		HashMap<Integer, Integer> suidOnId = new HashMap<Integer, Integer>();

		// extract all rows
		List<CyRow> rows = table.getAllRows();
		List<HashMap<String, Object>> mapList = new ArrayList<HashMap<String, Object>>();


		for (int i = 0; i < rows.size(); i++) {
			CyRow row = rows.get(i);
			Long suid = row.get("SUID", Long.class);
			// Get the SUID for corresponding Line (i.e. SUID of node/edge)

			// Generate a new HashMap for Data of node/edge
			HashMap<String, Object> data = new HashMap<>();


			// For nodes, extract the color from the style
			CyNode node = network.getNode(suid);
			if (node == null) {
				continue;
			}
			data.putAll(getStyle(node));
			data.put("id", i);
			// for(CyTable enrichment: enrichments) {
			// List<CyRow> enRows = table.getAllRows();
			// for (int j=0; j>enRows.size();j++) {
			// CyRow enRow = enRows.get(j);
			// for(String name : (List<String>) enRow.getRaw("genes")) {
			// if(name.equals(row.getRaw("display name"))) {
			// data.put(name, node)
			// }
			// }
			// }
			// }
			suidOnId.put(node.getSUID().intValue(), i);

			// if (type == CyNode.class) {
			// CyNode node = network.getNode(suid);
			// data.putAll(getStyle(node));
			// data.put("id", i);
			// }
			data = util.writeData(data, columnsArray, row, skipNodeColumns);
			mapList.add(data);
		}
		Object[] output = new Object[] {(List<HashMap<String, Object>>) mapList, suidOnId};
		return output;
	}

}
