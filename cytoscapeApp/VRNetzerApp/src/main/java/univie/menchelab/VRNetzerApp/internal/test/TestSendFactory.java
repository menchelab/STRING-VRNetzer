package univie.menchelab.VRNetzerApp.internal.test;

import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.task.AbstractNetworkTaskFactory;
import org.cytoscape.work.TaskIterator;

public class TestSendFactory extends AbstractNetworkTaskFactory {

	final CyServiceRegistrar registrar;

	public TestSendFactory(final CyServiceRegistrar registrar) {
		this.registrar = registrar;
	}

	public TaskIterator createTaskIterator(CyNetwork net) {
		return new TaskIterator(new TestSend(registrar, net));
	}


};
