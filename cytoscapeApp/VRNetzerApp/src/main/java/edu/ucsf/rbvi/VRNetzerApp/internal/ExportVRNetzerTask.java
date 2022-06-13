package edu.ucsf.rbvi.VRNetzerApp.internal;

import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;
//import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.work.AbstractTask;
import org.cytoscape.work.TaskMonitor;
import org.cytoscape.application.CyApplicationManager;
import org.cytoscape.view.vizmap.VisualMappingManager;
import org.cytoscape.view.vizmap.VisualStyleFactory;
import org.cytoscape.view.vizmap.VisualStyle;
//import org.cytoscape.task.internal.export.network.CyNetworkViewWriter;
//import org.cytoscape.task.internal.vizmap.VizmapWriter;

// Export Table
// ExportEnrichmentTable
// Call already implemented Task
// MCLClusterTask

public class ExportVRNetzerTask extends AbstractTask {

	final CyServiceRegistrar registrar;
	final CyApplicationManager appManager;
	final VisualMappingManager mappingManager;
	final VisualStyleFactory styleFactory;
	private CyNetwork network;
	
//	private final VisualStyle style;

	public ExportVRNetzerTask(CyServiceRegistrar registrar, CyNetwork network) {
		this.network = network;
		this.registrar = registrar;
		appManager = registrar.getService(CyApplicationManager.class);
		mappingManager = registrar.getService(VisualMappingManager.class);
		styleFactory = registrar.getService(VisualStyleFactory.class);
	}

	public void run(TaskMonitor monitor) {
//		reg.getService(CyApplicationManager.class).getCurrentNetwork();
		monitor.setTitle("Export network for VRNetzer");
		// Get current network
//		network = appManager.getCurrentNetwork();
		if (network == null)
			return;
		VisualStyle myStyle = mappingManager.getCurrentVisualStyle();
		if (myStyle == null)
			myStyle = styleFactory.createVisualStyle("default");
		System.out.println("My network is: " + network.toString());
		System.out.println("My style is: "+ myStyle.toString());
		monitor.setStatusMessage(
				"Exporting network "+ network.toString() +
				"with style " + myStyle.toString() );
		// open export dialog
		// TODO
		// export current network as GraphML and current style as .XML
		// TODO
		// Use Default Taks implemented in Cytoscape
	}

}
