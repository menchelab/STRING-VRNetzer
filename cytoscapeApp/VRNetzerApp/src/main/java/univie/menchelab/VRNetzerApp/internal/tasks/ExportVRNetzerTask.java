package univie.menchelab.VRNetzerApp.internal.tasks;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import org.cytoscape.model.CyEdge;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyNode;
import org.cytoscape.model.CyTable;
import org.cytoscape.model.CyTableManager;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.work.AbstractTask;
import org.cytoscape.work.ObservableTask;
import org.cytoscape.work.ProvidesTitle;
import org.cytoscape.work.TaskMonitor;
import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.ListMultipleSelection;
import org.json.simple.JSONObject;
import univie.menchelab.VRNetzerApp.internal.util.ConstructJson;
import univie.menchelab.VRNetzerApp.internal.util.NetworkUtil;
import univie.menchelab.VRNetzerApp.internal.util.Timer;

public class ExportVRNetzerTask extends AbstractTask implements ObservableTask {

	final CyServiceRegistrar registrar;
	private CyNetwork network;
	private List<String> skipNodeColumns =
			new ArrayList<String>(Arrays.asList("stringdb::STRING style", "selected",
					"stringdb::namespace", "stringdb::enhancedLabel Passthrough", "@id"));
	private List<String> HideNodeColumns = new ArrayList<>(skipNodeColumns);
	private List<String> HideEdgeColumns = new ArrayList<String>(Arrays.asList("selected", "SUID"));
	private List<String> skipEdgeColumns = new ArrayList<String>(Arrays.asList("selected"));
	// TODO Change that the default name of the file is "untitled"
	@Tunable(description = "Save network as <fileName>.VRNetz",
			params = "input=false;fileCategory=network",
			tooltip = "<html>Note: for convenience spaces are replaced by underscores.</html>",
			required = true, exampleStringValue = "network.VRNetz", groups = ("File property"))

	public File fileName = null;

	@Tunable(description = "Node attributes for export.",
			longDescription = "Select the node table columns to be exported.",
			groups = ("Table values"))
	public ListMultipleSelection<String> nodeAttributeList = null;

	@Tunable(description = "Edge attributes for export.",
			longDescription = "Select the edge table columns.", groups = ("Table values"))
	public ListMultipleSelection<String> edgeAttributeList = null;

	// @Tunable(description = "Select namespace to export.", params =
	// "input=false",gravity = 2.0)
	// public String namespace = null; // Not so sure about that one.

	private CyNetworkView netView;

	public ExportVRNetzerTask(CyServiceRegistrar registrar, CyNetwork network,
			CyNetworkView netView) {
		try {
			fileName = new File(System.getProperty("user.home") + "/Desktop" + "/untitled.VRNetz");
		} catch (Exception e) {
			fileName = new File("utitled.VRNetz");
		}

		HideNodeColumns.addAll(Arrays.asList("SUID", "display name"));
		this.registrar = registrar;
		if (network != null) {
			this.network = network;
			nodeAttributeList = NetworkUtil.updateNodeEdgeAttributeList(network, nodeAttributeList,
					CyNode.class, HideNodeColumns);
			edgeAttributeList = NetworkUtil.updateNodeEdgeAttributeList(network, edgeAttributeList,
					CyEdge.class, HideEdgeColumns);
		}
		this.netView = netView;
	}

	// JSONObject nodesJson = exportFile.generateObject("nodes", nodesData);
	// JSONObject edgesJson = exportFile.generateObject("edges", edgesData);
	ArrayList<String> layouts = new ArrayList<String>();
	CyTableManager tableManager = null;
	Set<CyTable> tables = null;

	// @SuppressWarnings("unchecked")
	@Override
	public void run(TaskMonitor monitor) throws Exception {
		monitor.setTitle("Export Network as VRNetz");
		monitor.setProgress(0);
		List<String> selectedNodeAttributes = nodeAttributeList.getSelectedValues();
		List<String> selectedEdgeAtrributes = edgeAttributeList.getSelectedValues();

		for (String attr : nodeAttributeList.getPossibleValues()) {
			if (!selectedNodeAttributes.contains(attr)) {
				skipNodeColumns.add(attr);
			}
		}

		for (String attr : edgeAttributeList.getPossibleValues()) {
			if (!selectedEdgeAtrributes.contains(attr)) {
				skipEdgeColumns.add(attr);
			}
		}
		monitor.setProgress(0.2);
		if (fileName == null) {
			monitor.showMessage(TaskMonitor.Level.WARN,
					"No file destination provided to export the network to.");
			throw new RuntimeException("No file name provided!");
		}
		// Set Names
		String _fileName = fileName.getAbsolutePath();
		System.out.println(_fileName);
		_fileName = _fileName.replace(' ', '_');
		if (!_fileName.endsWith(".VRNetz"))
			_fileName += ".VRNetz";
		monitor.setProgress(0.3);
		ConstructJson exportFile = new ConstructJson(registrar, monitor, network, netView,
				skipNodeColumns, skipEdgeColumns);
		JSONObject networkJson = exportFile.constructOutput();
		monitor.setProgress(0.8);

		monitor.showMessage(TaskMonitor.Level.INFO, "Writing data of '" + network.toString() + "'");
		Timer exportTimer =
				new Timer("Writing Data of " + network.toString() + "to file " + _fileName + ". ",
						monitor, TaskMonitor.Level.INFO);
		exportTimer.start();

		writeObject(networkJson, _fileName); // TODO Improve the writing performance, if we need
												// more nodes to be
												// exported!
		exportTimer.stop();

		monitor.showMessage(TaskMonitor.Level.INFO, "Exported file to " + _fileName + ".");
		monitor.setProgress(1);
	}

	public void writeObject(JSONObject myObject, String fileName) throws IOException {
		Files.write(Paths.get(fileName), myObject.toJSONString().getBytes());
		System.out.println(Paths.get(fileName));
	};

	@ProvidesTitle
	public String getTitle() {
		return "Export Network as VRNetz";
	}

	@Override
	public <R> R getResults(Class<? extends R> type) {
		return null;
	}
}
