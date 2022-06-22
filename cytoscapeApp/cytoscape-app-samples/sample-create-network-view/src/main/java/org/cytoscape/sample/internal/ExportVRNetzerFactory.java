package org.cytoscape.sample.internal;

import org.cytoscape.task.AbstractNetworkTaskFactory;
import org.cytoscape.work.TaskIterator;
import org.cytoscape.work.TaskMonitor;
import org.cytoscape.application.CyApplicationManager;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.view.vizmap.VisualMappingManager;
import org.cytoscape.view.vizmap.VisualStyleFactory;

public class ExportVRNetzerFactory extends AbstractNetworkTaskFactory {

	private final CyApplicationManager cyApplicationManager;
	private final VisualMappingManager visualMappingManager;
	private final VisualStyleFactory visualStyleFactory;
	
	public ExportVRNetzerFactory(
			CyApplicationManager cyApplicationManager,
			VisualMappingManager visualMappingManager,
			VisualStyleFactory visualStyleFactory
			){
		this.cyApplicationManager = cyApplicationManager;
		this.visualMappingManager = visualMappingManager;
		this.visualStyleFactory = visualStyleFactory;
	}

	@Override
	public TaskIterator createTaskIterator(CyNetwork network) {
		// TODO Auto-generated method stub
		return null;
	}
	
}
