package org.cytoscape.sample.internal;


import org.cytoscape.model.CyNetwork;
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

public class ExportVRNetzerProjectTask extends AbstractTask {

	private final CyApplicationManager appManager;
	private final VisualMappingManager mappingManager;
	private final VisualStyleFactory styleFactory;
//	private final VisualStyle style;

	public ExportVRNetzerProjectTask(CyApplicationManager appManager,
			VisualMappingManager styleManager,
			VisualStyleFactory styleFactory) {
		this.appManager = appManager;
		this.mappingManager = styleManager;
		this.styleFactory = styleFactory;
//		this.style = style;
	}

	public void run(TaskMonitor monitor) {
//		reg.getService(CyApplicationManager.class).getCurrentNetwork();
		monitor.setTitle("Export network for VRNetzer");
		// Get current network
		CyNetwork myNet = appManager.getCurrentNetwork();
		if (myNet == null)
			return;
		VisualStyle myStyle = mappingManager.getCurrentVisualStyle();
		if (myStyle == null)
			myStyle = styleFactory.createVisualStyle("default");
		System.out.println("My network is:" + myNet.toString());
		System.out.println("My style is:"+ myStyle.toString());
		monitor.setStatusMessage(
				"Exporting network "+ myNet.toString() +
				"with style " + myStyle.toString() );
		// open export dialog
		// TODO
		// export current network as GraphML and current style as .XML
		// TODO
		// Use Default Taks implemented in Cytoscape
	}

}
