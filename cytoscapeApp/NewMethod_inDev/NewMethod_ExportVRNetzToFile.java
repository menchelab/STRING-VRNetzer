package univie.menchelab.VRNetzerApp.internal.main;

import java.io.File;
import java.io.OutputStream;

import org.cytoscape.io.write.CyWriter;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.task.AbstractNetworkTask;
import org.cytoscape.work.TaskMonitor;
import org.cytoscape.work.Tunable;
import org.json.simple.JSONObject;

import univie.menchelab.VRNetzerApp.internal.util.ConstructJson;
import univie.menchelab.VRNetzerApp.internal.main.NewMethod_VRNetzExporter;
import org.cytoscape.io.CyFileFilter;


/**
 * Writer for VRNetz format
 * 
 */
public class NewMethod_ExportVRNetzToFile extends AbstractNetworkTask implements CyWriter {

	private final OutputStream outputStream;
	final CyServiceRegistrar registrar;
	private CyNetwork network;
	private JSONObject networkJson;
	
	@Tunable(description = "Save network as <fileName>.VRNetz", params = "input=false", 
	         tooltip="<html>Note: for convenience spaces are replaced by underscores.</html>",gravity = 1.0)
	public File fileName = null;


	public NewMethod_ExportVRNetzToFile(final OutputStream outputStream, final CyNetwork network, CyServiceRegistrar registrar) {
		super(network);
		this.outputStream = outputStream;
		this.registrar = registrar;
	}

	@Override
	public void run(TaskMonitor monitor) throws Exception {
		if (monitor != null) {
			monitor.setTitle("Writing to VRNetz");
			monitor.setStatusMessage("Writing network in .VRNetz format...");
			monitor.setProgress(-1.0);
		}
		NewMethod_VRNetzExporter exporter = new NewMethod_VRNetzExporter();
		
		if (monitor != null) {
			monitor.setStatusMessage("Success.");
			monitor.setProgress(1.0);
		}
	
	}
}