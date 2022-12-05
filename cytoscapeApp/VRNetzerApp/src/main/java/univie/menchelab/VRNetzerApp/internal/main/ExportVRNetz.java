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
import org.cytoscape.io.CyFileFilter;


/**
 * Writer for VRNetz format
 * 
 */
public class ExportVRNetz extends AbstractNetworkTask implements CyWriter{

	final CyServiceRegistrar registrar;
	private CyNetwork network;
	private JSONObject networkJson;
	
	@Tunable(description = "Save network as <fileName>.VRNetz", params = "input=false", 
	         tooltip="<html>Note: for convenience spaces are replaced by underscores.</html>",gravity = 1.0)
	public File fileName = null;


	public ExportVRNetz(final CyNetwork network, CyServiceRegistrar registrar) {
		super(network);
		this.registrar = registrar;
	}

	@Override
	public void run(TaskMonitor monitor) throws Exception {
		if (monitor != null) {
			monitor.setTitle("Writing to VRNetz");
			monitor.setStatusMessage("Writing network in .VRNetz format...");
			monitor.setProgress(-1.0);
		}
		
		NetworkToVRNetz writer = new NetworkToVRNetz(registrar,network);
		networkJson = writer.getVRNetz(monitor, fileName);
		

		
		if (monitor != null) {
			monitor.setStatusMessage("Success.");
			monitor.setProgress(1.0);
		}
	
	}
}