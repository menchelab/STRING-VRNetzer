package edu.ucsf.rbvi.VRNetzerApp.internal.main;

import org.cytoscape.task.NetworkTaskFactory;
import org.osgi.framework.BundleContext;
import org.cytoscape.service.util.AbstractCyActivator;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.application.CyApplicationManager;
import org.cytoscape.view.vizmap.VisualMappingManager;
import org.cytoscape.view.vizmap.VisualStyleFactory;
import static org.cytoscape.work.ServiceProperties.COMMAND;
//import static org.cytoscape.work.ServiceProperties.COMMAND_DESCRIPTION;
//import static org.cytoscape.work.ServiceProperties.COMMAND_EXAMPLE_JSON;
//import static org.cytoscape.work.ServiceProperties.COMMAND_LONG_DESCRIPTION;
import static org.cytoscape.work.ServiceProperties.COMMAND_NAMESPACE;
//import static org.cytoscape.work.ServiceProperties.COMMAND_SUPPORTS_JSON;
import static org.cytoscape.work.ServiceProperties.IN_MENU_BAR;
import static org.cytoscape.work.ServiceProperties.MENU_GRAVITY;
import static org.cytoscape.work.ServiceProperties.PREFERRED_MENU;
import static org.cytoscape.work.ServiceProperties.TITLE;
import static org.cytoscape.work.ServiceProperties.INSERT_SEPARATOR_BEFORE;
import java.util.Properties;

public class CyActivator extends AbstractCyActivator {
	public CyActivator() {
		super();
	}


	public void start(BundleContext bc) {
		CyServiceRegistrar registrar = getService(bc, CyServiceRegistrar.class);
	
		CyApplicationManager cyApplicationManager = getService(bc,CyApplicationManager.class);
		VisualMappingManager visualMappingManager = getService(bc,VisualMappingManager.class);
		VisualStyleFactory visualStyleFactory = getService(bc,VisualStyleFactory.class);
		ExportVRNetzerFactory exportNetwork = new ExportVRNetzerFactory(registrar);
		ExportVRNetzerFactory exportNetworkApp = new ExportVRNetzerFactory(registrar);
		
		Properties props = new Properties();
		props.setProperty(PREFERRED_MENU,"File.Export");
		props.setProperty(TITLE,"Network as VRNetz...");
		props.setProperty(MENU_GRAVITY,"4.0");
		
		// Create button on File -> Export -> Export network as VRNetz
		registerService(bc, exportNetwork, NetworkTaskFactory.class, props);
		
		props.setProperty(PREFERRED_MENU,"Apps.VRNetzer");
		props.setProperty(TITLE,"Export Network as VRNetz...");
		props.setProperty(MENU_GRAVITY,"1.0");
		
		// Create button on Apps -> VRNetzer -> Export as VRNetz
		registerService(bc, exportNetworkApp, NetworkTaskFactory.class, props);
				
		// TODO Command property to execute command in cmd line and as CyREST Call
		// TODO Add as second menu object as second instance
	}
	
}

