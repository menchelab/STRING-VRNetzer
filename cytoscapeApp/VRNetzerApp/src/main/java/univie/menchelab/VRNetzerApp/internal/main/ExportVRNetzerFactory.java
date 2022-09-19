package univie.menchelab.VRNetzerApp.internal.main;

import org.cytoscape.task.AbstractNetworkTaskFactory;
import org.cytoscape.work.TaskIterator;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;

public class ExportVRNetzerFactory extends AbstractNetworkTaskFactory {

	private CyServiceRegistrar registrar;
	
	public ExportVRNetzerFactory(
			CyServiceRegistrar registrar
			){
		this.registrar = registrar;
	}

	@Override
	public TaskIterator createTaskIterator(CyNetwork network) {
		return new TaskIterator(new ExportVRNetzerTask(registrar,network));
	}
	
}
