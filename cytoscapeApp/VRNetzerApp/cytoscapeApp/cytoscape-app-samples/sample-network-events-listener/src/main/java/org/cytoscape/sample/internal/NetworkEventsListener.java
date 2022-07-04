package org.cytoscape.sample.internal;


import org.cytoscape.model.events.AddedNodesEvent;
import org.cytoscape.model.events.AddedNodesListener;
import org.cytoscape.model.events.NetworkAboutToBeDestroyedEvent;
import org.cytoscape.model.events.NetworkAboutToBeDestroyedListener;
import org.cytoscape.model.events.NetworkAddedEvent;
import org.cytoscape.model.events.NetworkAddedListener;
import org.cytoscape.view.model.events.NetworkViewAddedEvent;
import org.cytoscape.view.model.events.NetworkViewAddedListener;


public class NetworkEventsListener implements NetworkAddedListener, NetworkAboutToBeDestroyedListener,
				NetworkViewAddedListener, AddedNodesListener {
	
	public void handleEvent(NetworkAddedEvent e){
		System.out.println("sample-network-events-listener: NetworkAddedEvent is received");
		System.out.println("\tnetwork name is "+ e.getNetwork().getRow(e.getNetwork()).get("name", String.class));
	}

	public void handleEvent(NetworkAboutToBeDestroyedEvent e){
		System.out.println("sample-network-events-listener: NetworkAboutToBeDestroyedEvent is received");
	}
	
	public void handleEvent(NetworkViewAddedEvent e){
		System.out.println("sample-network-events-listener: NetworkViewAddedEvent is received.");		
	}

	public void handleEvent(AddedNodesEvent e){
		System.out.println("sample-network-events-listener: AddedNodesEvent is received.");
	}	
}
