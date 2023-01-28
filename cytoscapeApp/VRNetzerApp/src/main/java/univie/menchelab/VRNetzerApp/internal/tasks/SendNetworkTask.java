package univie.menchelab.VRNetzerApp.internal.tasks;

import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Set;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyTable;
import org.cytoscape.model.CyTableManager;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.work.AbstractTask;
import org.cytoscape.work.ContainsTunables;
import org.cytoscape.work.ObservableTask;
import org.cytoscape.work.ProvidesTitle;
import org.cytoscape.work.TaskMonitor;
import org.cytoscape.work.TaskMonitor.Level;
import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.ListSingleSelection;
import org.json.simple.JSONObject;
import univie.menchelab.VRNetzerApp.internal.util.AlgorithmContext;
import univie.menchelab.VRNetzerApp.internal.util.ConstructJson;
import univie.menchelab.VRNetzerApp.internal.util.ExportContext;
import univie.menchelab.VRNetzerApp.internal.util.LayoutParamsContext;
import univie.menchelab.VRNetzerApp.internal.util.MessagePromptAction;
import univie.menchelab.VRNetzerApp.internal.util.SpringContext;
import univie.menchelab.VRNetzerApp.internal.util.TSNEContext;
import univie.menchelab.VRNetzerApp.internal.util.UMAPContext;
import univie.menchelab.VRNetzerApp.internal.util.Utility;
import univie.menchelab.VRNetzerApp.internal.util.http.ConnectionException;
import univie.menchelab.VRNetzerApp.internal.util.http.HttpUtil;

public class SendNetworkTask extends AbstractTask implements ObservableTask {

	final CyServiceRegistrar registrar;
	public CyNetwork network;

	@ContainsTunables
	public ExportContext exportContext = null;

	final String PROJECT_DESC =
			"Name which will be used to create a new project on the VRNetzer. If the project already exists, depending whether overwrite or update is selected, the files in the project will be overwritten or updated.Spaces will be replaced by underscores.";
	@Tunable(description = "Project name:", required = true, exampleStringValue = "new project",
			groups = {"VRNetzer variables", "Project"}, tooltip = PROJECT_DESC,
			longDescription = PROJECT_DESC, gravity = 1)
	public String projectName = "new project";

	final String UO_DESC =
			"Update will add any new layout to the project and will overwrite existing layouts with the same name.\nOverwrite will overwrite the whole project and will delete all layouts in the project.";
	@Tunable(description = "Update or Overwrite:", groups = {"VRNetzer variables", "Project"},
			gravity = 2, longDescription = UO_DESC, tooltip = UO_DESC)
	public ListSingleSelection<String> updateProject = new ListSingleSelection<String>(
			new ArrayList<String>(Arrays.asList("Update", "Overwrite")));

	final String LOAD_DESC =
			"If this is turned on, the project will be loaded up on running VRNetzer session.";
	@Tunable(description = "Load project:", longDescription = LOAD_DESC,
			groups = {"VRNetzer variables", "Project"}, tooltip = LOAD_DESC, gravity = 3)
	public Boolean load = false;

	final String IP_DESC = "IP of the VRNetzer, e.g. localhost";
	@Tunable(description = "IP of the VRNetzer:", required = true,
			groups = {"VRNetzer variables", "Connection config"}, tooltip = IP_DESC, gravity = 4,
			params = "displayState=expanded", longDescription = IP_DESC)
	public String ip = "localhost";

	final String PORT_DESC =
			"Port of the VRNetzer, default for Windows and Linux is 5000, for Mac its 3000";
	@Tunable(description = "Port of the VRNetzer:", required = true, tooltip = PORT_DESC,
			longDescription = PORT_DESC, groups = {"VRNetzer variables", "Connection config"},
			gravity = 5, params = "displayState=expanded")
	public Integer port = 5000;

	@ContainsTunables
	public AlgorithmContext algorithmContext = null;

	@ContainsTunables
	public SpringContext springContext = null;

	@ContainsTunables
	public UMAPContext umapContext = null;

	@ContainsTunables
	public TSNEContext tsneContext = null;

	@ContainsTunables
	public LayoutParamsContext layoutParamsContext = null;

	private CyNetworkView netView;


	public SendNetworkTask(CyServiceRegistrar registrar, CyNetwork network) {
		this.registrar = registrar;
		this.network = network;
		this.exportContext = new ExportContext();
		this.algorithmContext = new AlgorithmContext();
		this.springContext = new SpringContext();
		this.umapContext = new UMAPContext();
		this.tsneContext = new TSNEContext();
		this.layoutParamsContext = new LayoutParamsContext(springContext, umapContext, tsneContext);

		Utility.validate(network, netView, registrar);
		exportContext.setup(network, registrar);

	}

	// JSONObject nodesJson = exportFile.generateObject("nodes", nodesData);
	// JSONObject edgesJson = exportFile.generateObject("edges", edgesData);
	ArrayList<String> layouts = new ArrayList<String>();
	CyTableManager tableManager = null;
	Set<CyTable> tables = null;

	// @SuppressWarnings("unchecked")
	@Override
	public void run(TaskMonitor monitor) {
		projectName = projectName.replaceAll(" ", "_");
		monitor.setTitle("Send Network to VRNetzer");
		monitor.setProgress(0);


		monitor.setProgress(0.3);
		System.out.println("Test");
		ConstructJson constructJson = new ConstructJson(registrar, network, exportContext);

		JSONObject networkJson = constructJson.constructOutput();
		System.out.println("Test");
		HashMap<String, Object> formValues = new HashMap<String, Object>();
		HashMap<String, Object> algorithm_var = new HashMap<String, Object>();

		algorithm_var.put("n", algorithmContext.selectedLayout());
		algorithm_var.put("string_cg_prplxty", tsneContext.prplxty.getValue());
		algorithm_var.put("string_cg_density", tsneContext.density.getValue());
		algorithm_var.put("string_cg_l_rate", tsneContext.lRate.getValue());
		algorithm_var.put("string_cg_steps", tsneContext.steps.getValue());

		algorithm_var.put("string_cg_n_neighbors", umapContext.neighbors.getValue());
		algorithm_var.put("string_cg_spread", umapContext.spread.getValue());
		algorithm_var.put("string_cg_min_dist", umapContext.minDist.getValue());

		algorithm_var.put("string_spring_opt_dist", springContext.optDist.getValue());
		algorithm_var.put("string_spring_iterations", springContext.iter.getValue());
		algorithm_var.put("string_spring_threshold", springContext.iter.getValue());


		formValues.put("project", projectName);
		formValues.put("algorithm", algorithm_var);
		formValues.put("update", updateProject.getSelectedValue());
		formValues.put("layout", algorithmContext.getLayoutName());
		formValues.put("load", load);
		networkJson.put("form", formValues);

		monitor.setProgress(0.8);

		String baseURL = "http://" + ip + ":" + port.toString();

		JSONObject results = new JSONObject();
		// JSONObject results;
		try {
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
