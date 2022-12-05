package univie.menchelab.VRNetzerApp.internal.main;

import org.cytoscape.task.AbstractNetworkTaskFactory;
import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.work.TaskIterator;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.io.write.CyNetworkViewWriterFactory;
import org.cytoscape.io.write.CyWriter;

import java.io.OutputStream;

import org.cytoscape.io.CyFileFilter;

public class ExportVRNetzToFileFactory implements CyNetworkViewWriterFactory{

	private CyServiceRegistrar registrar;
	private CyFileFilter filter;
	
	
	public ExportVRNetzToFileFactory(
			CyServiceRegistrar registrar,
			CyFileFilter filter
			){
		this.registrar = registrar;
		this.filter = filter;
	}
		@Override
		public CyWriter createWriter(OutputStream outputStream, CyNetworkView view) {
			return new ExportVRNetzToFile(outputStream, view.getModel(), registrar);
		}
		
		@Override
		public CyWriter createWriter(OutputStream outputStream, CyNetwork network) {
			return new ExportVRNetzToFile(outputStream, network, registrar);
		}

		@Override
		public CyFileFilter getFileFilter() {
			return filter;
		}
//		@Override
//		public TaskIterator createTaskIterator(CyNetwork network) {
//			return new TaskIterator(new ExportVRNetzerTask(registrar,network));
//		}
	
}
