package univie.menchelab.VRNetzerApp.internal.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.cytoscape.model.CyEdge;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyNode;
import org.cytoscape.model.CyTable;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.work.ContainsTunables;
import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.ListMultipleSelection;

public class ExportContext {

	CyNetwork network = null;
	CyServiceRegistrar registrar = null;
	String networkType = null;

	final String NODE_DESC = "Select the table columns which should be exported.";
	@Tunable(description = "Node attributes for export.", tooltip = NODE_DESC,
			longDescription = NODE_DESC, groups = {"Data tables"},
			params = "displayState=collapsed", gravity = 19)
	public ListMultipleSelection<String> nodeAttributeList = null;

	final String EDGE_DESC = "Select the table columns which should be exported.";
	@Tunable(description = "Edge attributes for export.", tooltip = EDGE_DESC,
			longDescription = EDGE_DESC, groups = {"Data tables"},
			params = "displayState=collapsed", gravity = 20)
	public ListMultipleSelection<String> edgeAttributeList = null;

	@ContainsTunables
	public StringNetworkContext stringContext = null;

	List<String> selectedNodeAttributes, selectedEdgeAttributes = null;


	public List<String> skipNodeColumns =
			new ArrayList<String>(Arrays.asList("stringdb::STRING style", "selected",
					"stringdb::namespace", "stringdb::enhancedLabel Passthrough", "@id"));

	public List<String> skipEdgeColumns = new ArrayList<String>(Arrays.asList("selected"));
	public List<String> skipNetworkColumns =
			new ArrayList<String>(Arrays.asList("selected", "analyzedNodes.SUID"));

	public List<String> HideNodeColumns = new ArrayList<>(skipNodeColumns);
	public List<String> HideEdgeColumns = new ArrayList<String>(Arrays.asList("selected", "SUID"));

	public void setup(CyNetwork network, CyServiceRegistrar registrar) {
		this.network = network;
		this.registrar = registrar;
		updateAttributes();
		CyTable networkInfo = network.getTable(CyNetwork.class, CyNetwork.LOCAL_ATTRS);
		this.networkType = networkInfo.getRow(network.getSUID()).get("database", String.class);

		if (networkType != null && networkType.equals("string")) {
			stringContext = new StringNetworkContext();
			stringContext.setup(network, registrar);
		}

	}

	public void updateAttributes() {
		HideNodeColumns.addAll(Arrays.asList("SUID", "display name"));
		nodeAttributeList = NetworkUtil.updateNodeEdgeAttributeList(network, nodeAttributeList,
				CyNode.class, HideNodeColumns);
		edgeAttributeList = NetworkUtil.updateNodeEdgeAttributeList(network, edgeAttributeList,
				CyEdge.class, HideEdgeColumns);
	}

	public void filterAttributes() {
		selectedNodeAttributes = nodeAttributeList.getSelectedValues();
		selectedEdgeAttributes = edgeAttributeList.getSelectedValues();

		skipNodeColumns.addAll(Utility.getFilteredList(nodeAttributeList, selectedNodeAttributes));
		skipEdgeColumns.addAll(Utility.getFilteredList(edgeAttributeList, selectedEdgeAttributes));

	}

}
