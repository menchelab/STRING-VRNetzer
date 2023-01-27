package univie.menchelab.VRNetzerApp.internal.tasks;

import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
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
import org.cytoscape.work.TaskMonitor.Level;
import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.ListMultipleSelection;
import org.cytoscape.work.util.ListSingleSelection;
import org.json.simple.JSONObject;
import univie.menchelab.VRNetzerApp.internal.util.ConstructJson;
import univie.menchelab.VRNetzerApp.internal.util.MessagePromptAction;
import univie.menchelab.VRNetzerApp.internal.util.NetworkUtil;
import univie.menchelab.VRNetzerApp.internal.util.http.ConnectionException;
import univie.menchelab.VRNetzerApp.internal.util.http.HttpUtil;

public class SendNetworkTask extends AbstractTask implements ObservableTask {

	final CyServiceRegistrar registrar;
	private CyNetwork network;
	private List<String> skipNodeColumns =
			new ArrayList<String>(Arrays.asList("stringdb::STRING style", "selected",
					"stringdb::namespace", "stringdb::enhancedLabel Passthrough", "@id"));
	private List<String> HideNodeColumns = new ArrayList<>(skipNodeColumns);
	private List<String> HideEdgeColumns = new ArrayList<String>(Arrays.asList("selected", "SUID"));
	private List<String> skipEdgeColumns = new ArrayList<String>(Arrays.asList("selected"));
	// TODO Change that the default name of the file is "untitled"
	@Tunable(description = "Project name:", required = true, exampleStringValue = "new project",
			groups = {"VRNetzer variables", "Project"})
	public String projectName = "new project";

	@Tunable(description = "Update or Overwrite:", groups = {"VRNetzer variables", "Project"})
	public ListSingleSelection updateProject = new ListSingleSelection<String>();

	@Tunable(description = "Load project:",
			longDescription = "If this is turned on, the project will be loaded up on running VRNetzer session.",
			groups = {"VRNetzer variables"},
			tooltip = "If this is turned on, the project will be loaded up on running VRNetzer session.")
	public Boolean load = false;

	@Tunable(description = "Layout algorithm:", required = true, exampleStringValue = "new project",
			groups = {"VRNetzer variables", "Project"})
	public ListSingleSelection<String> algorithm = new ListSingleSelection<String>();

	@Tunable(description = "Layout name", required = true, exampleStringValue = "spring_layout",
			groups = {"VRNetzer variables", "Project"})
	public String layoutName = null;

	@Tunable(description = "IP of the VRNetzer:", required = true, groups = {"VRNetzer variables"})
	public String ip = "localhost";

	@Tunable(description = "Port of the VRNetzer:", required = true,
			groups = {"VRNetzer variables"})
	public Integer port = 5000;

	@Tunable(description = "Node attributes for export.",
			longDescription = "Select the node table columns to be exported.",
			groups = ("Table values"))
	public ListMultipleSelection<String> nodeAttributeList = null;

	@Tunable(description = "Edge attributes for export.",
			longDescription = "Select the edge table columns.", groups = ("Table values"))
	public ListMultipleSelection<String> edgeAttributeList = null;

	// @Tunable(description = "Select namespace to export.", params = "input=false",gravity = 2.0)
	// public String namespace = null; // Not so sure about that one.

	private CyNetworkView netView;


	public SendNetworkTask(CyServiceRegistrar registrar, CyNetwork network, CyNetworkView netView) {

		HideNodeColumns.addAll(Arrays.asList("SUID", "display name"));
		this.registrar = registrar;
		if (network != null) {
			this.network = network;
			nodeAttributeList = NetworkUtil.updateNodeEdgeAttributeList(network, nodeAttributeList,
					CyNode.class, HideNodeColumns);
			edgeAttributeList = NetworkUtil.updateNodeEdgeAttributeList(network, edgeAttributeList,
					CyEdge.class, HideEdgeColumns);
			algorithm.setPossibleValues(new ArrayList<String>(
					Arrays.asList("spring", "kamada_kawai", "cg_local_tsne", "cg_global_tsne",
							"cg_global_umap", "cg_importance_umap", "cg_importance_umap")));
			algorithm.setSelectedValue("spring");
			updateProject
					.setPossibleValues(new ArrayList<String>(Arrays.asList("Update", "Overwrite")));
			updateProject.setSelectedValue("Update");
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
		monitor.setTitle("Send Network to VRNetzer");
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

		monitor.setProgress(0.3);
		ConstructJson constructJson = new ConstructJson(registrar, monitor, network, netView,
				skipNodeColumns, skipEdgeColumns);
		JSONObject networkJson = constructJson.constructOutput();
		HashMap<String, Object> formValues = new HashMap<String, Object>();
		HashMap<String, String> algorithm_var = new HashMap<String, String>();

		algorithm_var.put("n", algorithm.getSelectedValue());

		formValues.put("project", projectName);
		formValues.put("algorithm", algorithm_var);
		formValues.put("update", updateProject.getSelectedValue());
		formValues.put("layout", layoutName);
		formValues.put("load", load);

		networkJson.put("form", formValues);

		monitor.setProgress(0.8);

		String baseURL = "http://" + ip + ":" + port.toString();

		JSONObject results;
		try {
			// results = HttpUtils.postJSON(getExampleJsonNetwork(), registrar);
			String URL = baseURL + "/StringEx/receiveNetwork";
			results = HttpUtil.postJSON(networkJson, registrar, URL);
			String href = baseURL + "/StringEx/preview?project=" + projectName;
			String message = "Network sent to VRNetzer.<br><h4><a style='color:green;'href=" + href
					+ ">Preview project: '" + projectName + "' on VRNetzer platform -></a></h4>";
			message += "<br>" + results.get("html").toString();
			presentResults(monitor, baseURL, message);
			monitor.setProgress(1.0);
		} catch (ConnectionException e) {
			String message = "Could not connect to VRNetzer platform.<br>Project '" + projectName
					+ "' has not been uploaded.<br>Please check you ip and port: <a href=" + baseURL
					+ ">" + baseURL + "</a>";

			message = "<h4 style='color:red'>Network error:</h4><br>" + "<p>" + e.getMessage()
					+ "<br><p>" + message + "</p>";
			presentResults(monitor, baseURL, message);
			monitor.setProgress(1.0);
			return;
		}


	}

	public void presentResults(TaskMonitor monitor, String baseURL, String message) {
		URL stream = getClass().getResource("/VRNetzerStyle.css");
		System.out.println(stream);
		String style = "<link rel='stylesheet' href='" + stream + "'/>";

		String html = "<html><head>";
		html += style;
		html += "</head><body>";
		html += message;
		html += "</body></html>";

		monitor.showMessage(Level.INFO, message);

		MessagePromptAction resultPanel = new MessagePromptAction(registrar, html);
		resultPanel.actionPerformed(null);

	}

	@ProvidesTitle
	public String getTitle() {
		return "Export Network as VRNetz";
	}

	@Override
	public <R> R getResults(Class<? extends R> type) {
		return null;
	}
}
