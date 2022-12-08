package univie.menchelab.VRNetzerApp.internal.main;
public final class NewMethod_VRNetzExporter extends AbstractNetworkTask implements CyWriter {
	private CyNetwork network;
	private CyNetworkView netView;
	private final OutputStream outputStream;
	private CyServiceRegistrar registrar;
	private File fileName;
	JSONObject networkJson = new JSONObject();
	
	public NewMethod_VRNetzExporter(OutputStream outputStream,CyNetwork network,CyServiceRegistrar registrar,File fileName) {
		super(network);
		this.outputStream = outputStream;
		this.registrar = registrar;
		this.fileName = fileName;
	};
	@Override
	public void run(TaskMonitor monitor) throws Exception {
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
		NewMethod_NetworkToVRNetz networkToJson = new NewMethod_NetworkToVRNetz(registrar,network);
		networkJson = networkToJson.getVRNetz(monitor);
		
		// Write data to json
		monitor.showMessage(TaskMonitor.Level.INFO, "Writing data of '"+network.toString()+"'");
        long startTime = System.currentTimeMillis();
        
        OutputStreamWriter writer = new OutputStreamWriter(outputStream,Charset.forName("UTF-8").newEncoder());
        
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
		outputStream.close();
		
	}
}
