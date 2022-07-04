package org.cytoscape.sample.internal;

/*
 * #%L
 * Cytoscape Linkout Impl (linkout-impl)
 * $Id:$
 * $HeadURL:$
 * %%
 * Copyright (C) 2006 - 2013 The Cytoscape Consortium
 * %%
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as 
 * published by the Free Software Foundation, either version 2.1 of the 
 * License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Lesser Public License for more details.
 * 
 * You should have received a copy of the GNU General Lesser Public 
 * License along with this program.  If not, see
 * <http://www.gnu.org/licenses/lgpl-2.1.html>.
 * #L%
 */

//import org.cytoscape.application.CyApplicationConfiguration;
//import org.cytoscape.work.SynchronousTaskManager;
//import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.property.CyProperty;
import org.cytoscape.service.util.AbstractCyActivator;
import org.osgi.framework.BundleContext;


import org.cytoscape.sample.internal.MyServiceListener;


public class CyActivator extends AbstractCyActivator {

	public CyActivator() {
		super();
	}

	public void start(BundleContext bc) {

		MyServiceListener myServiceListener = new MyServiceListener();
		
		registerServiceListener(bc, myServiceListener, "addPropertyService", "removePropertyService", CyProperty.class);		
	}
}

