package univie.menchelab.VRNetzerApp.internal.main;

import org.cytoscape.task.NetworkTaskFactory;
import org.osgi.framework.BundleContext;
import org.cytoscape.service.util.AbstractCyActivator;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.application.CyApplicationManager;
import org.cytoscape.io.BasicCyFileFilter;
import org.cytoscape.io.DataCategory;
import org.cytoscape.io.util.StreamUtil;
import org.cytoscape.view.vizmap.VisualMappingManager;
import org.cytoscape.view.vizmap.VisualStyleFactory;
import static org.cytoscape.work.ServiceProperties.COMMAND;
import static org.cytoscape.work.ServiceProperties.COMMAND_DESCRIPTION;
import static org.cytoscape.work.ServiceProperties.COMMAND_EXAMPLE_JSON;
import static org.cytoscape.work.ServiceProperties.COMMAND_LONG_DESCRIPTION;
//import static org.cytoscape.work.ServiceProperties.COMMAND_DESCRIPTION;
//import static org.cytoscape.work.ServiceProperties.COMMAND_EXAMPLE_JSON;
//import static org.cytoscape.work.ServiceProperties.COMMAND_LONG_DESCRIPTION;
import static org.cytoscape.work.ServiceProperties.COMMAND_NAMESPACE;
import static org.cytoscape.work.ServiceProperties.COMMAND_SUPPORTS_JSON;
//import static org.cytoscape.work.ServiceProperties.COMMAND_SUPPORTS_JSON;
import static org.cytoscape.work.ServiceProperties.IN_MENU_BAR;
import static org.cytoscape.work.ServiceProperties.MENU_GRAVITY;
import static org.cytoscape.work.ServiceProperties.PREFERRED_MENU;
import static org.cytoscape.work.ServiceProperties.TITLE;
import static org.cytoscape.work.ServiceProperties.INSERT_SEPARATOR_BEFORE;
import static org.cytoscape.work.ServiceProperties.ID;
import java.util.Properties;

public class NewMethod_CyActivator extends AbstractCyActivator {
	String JSON_EXAMPLE = "{\"SUID\":1234}";
	public NewMethod_CyActivator() {
		super();
	}


	public void start(BundleContext bc) {
		CyServiceRegistrar registrar = getService(bc, CyServiceRegistrar.class);
	
		CyApplicationManager cyApplicationManager = getService(bc,CyApplicationManager.class);
		VisualMappingManager visualMappingManager = getService(bc,VisualMappingManager.class);
		VisualStyleFactory visualStyleFactory = getService(bc,VisualStyleFactory.class);
		StreamUtil streamUtil = getService(bc, StreamUtil.class);
		final BasicCyFileFilter fileFilter = new BasicCyFileFilter(new String[] { "VRNetz" },
				new String[] { "application/json" }, "JSON for VRNetzer", DataCategory.NETWORK, streamUtil);
		NewMethod_ExportVRNetzToFileFactory exportNetworkAsFile = new NewMethod_ExportVRNetzToFileFactory(registrar,fileFilter);
//		ExportVRNetzerFactory exportNetworkAPP = new ExportVRNetzerFactory(registrar);
//		final BasicCyFileFilter cytoscapejsFilter = new BasicCyFileFilter(new String[] { "VRNetz" },
//				new String[] { "application/VRNetz" }, "Cytoscape.VRNetz", DataCategory.NETWORK, streamUtil);
//		final Properties exportProp = new Properties();
//		exportProp.put(ID, "cytoscapejsNetworkWriterFactory");
//		registerService(bc, exportNetwork, NetworkTaskFactory.class, exportProp);
		
		Properties props = new Properties();
		
		// Create button on File -> Export -> Export network as VRNetz
//		props.setProperty(COMMAND_SUPPORTS_JSON, "true");
//    	props.setProperty(COMMAND_EXAMPLE_JSON, JSON_EXAMPLE);

//		
//		props.setProperty(PREFERRED_MENU,"File.Export");
//		props.setProperty(TITLE,"Network as VRNetz...");
//		props.setProperty(MENU_GRAVITY,"4.0");
		props.setProperty(ID,"exportVRNetzerFactory");
		
		registerAllServices(bc, exportNetworkAsFile, props);
		
		// Create button on Apps -> VRNetzer -> Export as VRNetz
		NewMethod_ExportVRNetzFactory exportNetwork = new NewMethod_ExportVRNetzFactory(registrar);
		props.setProperty(PREFERRED_MENU,"Apps.VRNetzer");
		props.setProperty(TITLE,"Export Network as VRNetz...");
		props.setProperty(MENU_GRAVITY,"1.0");
		
		props.setProperty(COMMAND_NAMESPACE, "vrnetzer");
		props.setProperty(COMMAND, "export");
		props.setProperty(COMMAND_DESCRIPTION, 
			    "Exports the currently selected network.");
		props.setProperty(COMMAND_LONG_DESCRIPTION,
				"<html>The currently selected network gets exported <br />"
				+ "as an VRNetz.<br /></html>");
		props.setProperty(ID, "vrnetzerExportApp");
		
		registerService(bc, exportNetwork, NetworkTaskFactory.class, props);
				
		// TODO Command property to execute command in cmd line and as CyREST Call
		// TODO Add as second menu object as second instance
	}
	
}

//https://github.com/keiono/cytoscape-d3/blob/master/src/main/java/org/cytoscape/d3/internal/writer/D3NetworkWriter.java
//https://github.com/cytoscape/cx/tree/49e178adef988405f723403ed144554f2be7c3c8/src/main/java/org/cytoscape/io/internal/cx_writer

