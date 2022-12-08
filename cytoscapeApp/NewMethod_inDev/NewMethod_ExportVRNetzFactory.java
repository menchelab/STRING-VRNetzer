package univie.menchelab.VRNetzerApp.internal.main;

import org.cytoscape.task.AbstractNetworkTaskFactory;
import org.cytoscape.work.TaskIterator;

import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;

public class NewMethod_ExportVRNetzFactory extends AbstractNetworkTaskFactory {

	private CyServiceRegistrar registrar;
	
	public NewMethod_ExportVRNetzFactory(
			CyServiceRegistrar registrar
			){
		this.registrar = registrar;
	}

	@Override
	public TaskIterator createTaskIterator(CyNetwork network) {
		return new TaskIterator(new NewMethod_ExportVRNetz(network,registrar));
	}
	
}