package univie.menchelab.VRNetzerApp.internal.main;

import java.io.OutputStreamWriter;
import java.util.Collection;

import org.cytoscape.model.CyNetwork;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.view.model.CyNetworkViewManager;
import org.cytoscape.work.TaskMonitor;
import org.json.simple.JSONObject;

import univie.menchelab.VRNetzerApp.internal.util.ConstructJson;

public final class VRNetzExporter {
	private CyNetwork network;
	private CyNetworkView netView;
	JSONObject networkJson = new JSONObject();
	
	public void VRNetzerExporter(CyNetwork network) {
		this.network = network;
		
	}
	public final void writeNetwork(TaskMonitor monitor, CyServiceRegistrar registrar) throws Exception {
        Collection<CyNetworkView> views = registrar.getService(CyNetworkViewManager.class).getNetworkViews(network);
        if (views.isEmpty()){
        	monitor.setTitle("Error: No network view!");
    	   monitor.showMessage(TaskMonitor.Level.ERROR,"You first have to create a network view!");
    	   throw new RuntimeException("You first have to create a network view!");
        }
        // Get NetView
        for (CyNetworkView view: views) {
            if (view.getRendererId().equals("org.cytoscape.ding")) {
            	netView = view;
                break;
            }
        }; 
		NetworkToVRNetz writer = new NetworkToVRNetz(registrar,network);
		networkJson = writer.getVRNetz(monitor);
		
		// Write data to json
		monitor.showMessage(TaskMonitor.Level.INFO, "Writing data of '"+network.toString()+"'");
        long startTime = System.currentTimeMillis();
        
        OutputStreamWriter writer = new OutputStreamWriter(outputStream,EncodingUtil.getEncoder());
		if (fileName == null) throw new RuntimeException("Output has no filename!");
		// Set Names
		String _fileName = fileName.getAbsolutePath();
		_fileName = _fileName.replace(' ','_');
		if (!_fileName.endsWith(".VRNetz"))
			_fileName += ".VRNetz";
		
		ConstructJson exportFile = new ConstructJson(_fileName);
		exportFile.writeObject(networkJson);
		
		long stopTime = System.currentTimeMillis();
        long totalTime = stopTime - startTime;
        double totalTimeInSeconds = (double) stopTime-startTime / 1_000_000_000;
        
		monitor.showMessage(TaskMonitor.Level.INFO, "Writing file took:"+String.valueOf(totalTimeInSeconds));
		
		monitor.setStatusMessage("Exported network to '"+_fileName+"'");
	}
}
