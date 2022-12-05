package univie.menchelab.VRNetzerApp.internal.main;

import org.cytoscape.task.AbstractNetworkTaskFactory;
import org.cytoscape.work.TaskIterator;

import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;

public class ExportVRNetzFactory extends AbstractNetworkTaskFactory {

	private CyServiceRegistrar registrar;
	
	public ExportVRNetzFactory(
			CyServiceRegistrar registrar
			){
		this.registrar = registrar;
	}

	@Override
	public TaskIterator createTaskIterator(CyNetwork network) {
		return new TaskIterator(new ExportVRNetz(network,registrar));
	}
	
}