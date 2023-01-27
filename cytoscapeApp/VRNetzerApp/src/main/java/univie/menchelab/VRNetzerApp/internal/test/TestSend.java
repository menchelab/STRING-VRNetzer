package univie.menchelab.VRNetzerApp.internal.test;

import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.work.AbstractTask;
import org.cytoscape.work.ObservableTask;
import org.cytoscape.work.TaskMonitor;
import univie.menchelab.VRNetzerApp.internal.tasks.SendNetworkTask;

public class TestSend extends AbstractTask implements ObservableTask {

	final CyServiceRegistrar registrar;
	private CyNetwork network;

	public TestSend(CyServiceRegistrar registrar, CyNetwork network) {
		this.registrar = registrar;
		this.network = network;
	}

	@Override
	public <R> R getResults(Class<? extends R> type) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void run(TaskMonitor taskMonitor) throws Exception {
		SendNetworkTask task = new SendNetworkTask(registrar, network, null);
		task.port = 3000;
		task.projectName = "CyTest";
		task.layoutName = "spring";
		task.load = true;
		task.run(taskMonitor);
	}

}
