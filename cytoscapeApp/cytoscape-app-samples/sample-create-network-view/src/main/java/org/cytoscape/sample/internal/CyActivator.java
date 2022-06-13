package org.cytoscape.sample.internal;

import org.cytoscape.task.NetworkTaskFactory;
import org.osgi.framework.BundleContext;
import org.cytoscape.service.util.AbstractCyActivator;
//import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.application.CyApplicationManager;
import org.cytoscape.view.vizmap.VisualMappingManager;
import org.cytoscape.view.vizmap.VisualStyleFactory;

import java.util.Properties;


public class CyActivator extends AbstractCyActivator {
	public CyActivator() {
		super();
	}


	public void start(BundleContext bc) {
//		CyServiceRegistrar registrar = getService(bc, CyServiceRegistrar.class);
		
		CyApplicationManager cyApplicationManager = getService(bc,CyApplicationManager.class);
		VisualMappingManager visualMappingManager = getService(bc,VisualMappingManager.class);
		VisualStyleFactory visualStyleFactory = getService(bc,VisualStyleFactory.class);
		ExportVRNetzerFactory exportVRNetzerProject = new ExportVRNetzerFactory(cyApplicationManager,
				visualMappingManager,visualStyleFactory);
				
		Properties createNetworkViewTaskFactoryProps = new Properties();
		createNetworkViewTaskFactoryProps.setProperty("preferredMenu","File.Export");
		createNetworkViewTaskFactoryProps.setProperty("title","Network to VRNetzer...");
		createNetworkViewTaskFactoryProps.setProperty("menuGravity","4.0");
		// TODO Command property to execute command in cmd line and as CyREST Call
		// TODO Make it unclickable if no network is selected.
		registerService(bc,exportVRNetzerProject,NetworkTaskFactory.class, createNetworkViewTaskFactoryProps);
		// TODO Add as second menu object as second instance
	}
	
}

