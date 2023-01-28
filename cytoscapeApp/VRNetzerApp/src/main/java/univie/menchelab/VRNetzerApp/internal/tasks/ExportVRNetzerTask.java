package univie.menchelab.VRNetzerApp.internal.tasks;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
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
import org.cytoscape.work.Tunable;
import org.json.simple.JSONObject;
import univie.menchelab.VRNetzerApp.internal.util.ConstructJson;
import univie.menchelab.VRNetzerApp.internal.util.ExportContext;
import univie.menchelab.VRNetzerApp.internal.util.Timer;
import univie.menchelab.VRNetzerApp.internal.util.Utility;

public class ExportVRNetzerTask extends AbstractTask implements ObservableTask {

	final CyServiceRegistrar registrar;
	private CyNetwork network;
	public TaskMonitor monitor = null;
	public String networkType = null;

	@ContainsTunables
	public ExportContext context = null;

	@Tunable(description = "Save network as ...", params = "input=false;fileCategory=network",
			tooltip = "<html>Note: for convenience spaces are replaced by underscores.</html>",
			required = true, exampleStringValue = "network.VRNetz", groups = ("File property"),
			gravity = 1.0)
	public File fileName = new File("untitled.VRNetz");

	public String _fileName = null;



	private CyNetworkView netView;

	public ExportVRNetzerTask(CyServiceRegistrar registrar, CyNetwork network) {
		// Check if network is not null
		Utility.validate(network, netView, registrar);
		validatedFileName();
		this.registrar = registrar;
		this.network = network;
		this.context = new ExportContext();
		context.setup(network, registrar);

	}

	CyTableManager tableManager = null;
	Set<CyTable> tables = null;

	// @SuppressWarnings("unchecked")
	@Override
	public void run(TaskMonitor monitor) throws Exception {
		this.monitor = monitor;
		monitor.setTitle("Export Network as VRNetz");
		monitor.setProgress(0);
		context.filterAttributes();


		monitor.setProgress(0.2);

		monitor.setProgress(0.3);
		ConstructJson exportFile = new ConstructJson(registrar, network, context);
		JSONObject networkJson = exportFile.constructOutput();
		monitor.setProgress(0.8);

		monitor.showMessage(TaskMonitor.Level.INFO, "Writing data of '" + network.toString() + "'");
		Timer exportTimer =
				new Timer("Writing Data of " + network.toString() + "to file " + _fileName + ". ",
						monitor, TaskMonitor.Level.INFO);
		exportTimer.start();

		writeObject(networkJson, _fileName);
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

	public void validatedFileName() {
		try {
			fileName = new File(System.getProperty("user.home") + "/Desktop" + "/untitled.VRNetz");
		} catch (Exception e) {
			System.out.println("Reset file name to default.");
			fileName = new File("untitled.VRNetz");
		}
		if (fileName == null) {
			throw new RuntimeException("No file name provided!");
		}
		// Set Names
		_fileName = fileName.getAbsolutePath();
		System.out.println(_fileName);
		_fileName = _fileName.replace(' ', '_');
		if (!_fileName.endsWith(".VRNetz"))
			_fileName += ".VRNetz";
	}
}
