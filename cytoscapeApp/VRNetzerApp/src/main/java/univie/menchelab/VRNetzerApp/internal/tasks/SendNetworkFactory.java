package univie.menchelab.VRNetzerApp.internal.tasks;

import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.task.AbstractNetworkTaskFactory;
import org.cytoscape.work.TaskIterator;

public class SendNetworkFactory extends AbstractNetworkTaskFactory {

	final CyServiceRegistrar registrar;

	public SendNetworkFactory(final CyServiceRegistrar registrar) {
		this.registrar = registrar;
	}

	public TaskIterator createTaskIterator(CyNetwork net) {
		return new TaskIterator(new SendNetworkTask(registrar, net));
	}


};
