package univie.menchelab.VRNetzerApp.internal.main;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.stream.Collectors;

import org.cytoscape.application.CyApplicationManager;
import org.cytoscape.io.internal.AspectSet;
import org.cytoscape.io.internal.CyServiceModule;
import org.cytoscape.io.internal.cxio.CxExporter;
import org.cytoscape.io.internal.cxio.CxUtil;
import org.cytoscape.io.internal.cxio.Settings;
import org.cytoscape.io.internal.cxio.TimingUtil;
import org.cytoscape.io.write.CyWriter;
import org.cytoscape.model.CyEdge;
import org.cytoscape.model.CyIdentifiable;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyNode;
import org.cytoscape.model.CyTable;
import org.cytoscape.model.subnetwork.CyRootNetwork;
import org.cytoscape.model.subnetwork.CySubNetwork;
import org.cytoscape.work.TaskMonitor;
import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.ListMultipleSelection;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * This class is an example on how to use CxExporter in a Cytoscape task.
 *
 * @author cmzmasek
 *
 */
public class NewMethod_VRNetzNetworkWriter implements CyWriter {

//	private final static Logger logger = LoggerFactory.getLogger(CxNetworkWriter.class);
	private static final boolean WRITE_SIBLINGS_DEFAULT = false;
	private static final boolean USE_CXID_DEFAULT = true;
	private final OutputStream _os;
	private final CyNetwork _network;

	public ListMultipleSelection<String> aspectFilter = new ListMultipleSelection<>();
	public ListMultipleSelection<String> nodeColFilter = new ListMultipleSelection<>();
	public ListMultipleSelection<String> edgeColFilter = new ListMultipleSelection<>();
	public ListMultipleSelection<String> networkColFilter = new ListMultipleSelection<>();

//	@Tunable(description = "Aspects")
//	public ListMultipleSelection<String> getAspectFilter() {
//		return aspectFilter;
//	}
//
//	@Tunable(description = "Node Columns")
//	public ListMultipleSelection<String> getNodeColFilter() {
//		return nodeColFilter;
//	}
//
//	@Tunable(description = "Edge Columns")
//	public ListMultipleSelection<String> getEdgeColFilter() {
//		return edgeColFilter;
//	}
//
//	@Tunable(description = "Network Columns")
//	public ListMultipleSelection<String> getNetworkColFilter() {
//		return networkColFilter;
//	}

	public boolean writeSiblings = WRITE_SIBLINGS_DEFAULT;

//    @Tunable(description = "Write all networks in the collection")
//    public Boolean getWriteSiblings() {
//        return writeSiblings;
//    }

    public void setWriteSiblings(Boolean writeSiblings) {
        this.writeSiblings = writeSiblings;
    }

	public boolean useCxId = USE_CXID_DEFAULT;

	@Tunable(description = "Use CX ID (recommended)", 
//			dependsOn = "writeSiblings=false", 
//			listenForChange = "writeSiblings",
//			tooltip="Element IDs (nodes, edges) do not normally persist when a network is " + 
//				"imported/exported from Cytoscape. Cytoscape uses Session Unique IDs (SUIDs) " +
//				"which are set incrementally. Check this box to persist element IDs (useful for scripting).")
//	public boolean getUseCxId() {
//		if (writeSiblings) {
//			return false;
//		}
//		final CyApplicationManager _application_manager = CyServiceModule.getService(CyApplicationManager.class);
//
//		if (!CxUtil.hasCxIds(_application_manager.getCurrentNetwork())) {
//			return false;
//		}
//		return useCxId;
//    }
    
    public void setUseCxId(final Boolean useCxId) {
        this.useCxId = useCxId;
    }

	public NewMethod_VRNetzNetworkWriter(final OutputStream os, final CyNetwork network) {

		_os = os;
		_network = network;

	}

	private final Set<String> getAllColumnNames(final Class<? extends CyIdentifiable> type, CyNetwork subnet){
		final SortedSet<String> colNames = new TreeSet<>();
		
		// Shared
		final CyTable sharedTable = subnet.getTable(type, CyNetwork.DEFAULT_ATTRS);
		colNames.addAll(sharedTable.getColumns().stream().map(col -> col.getName()).collect(Collectors.toList()));
		
		// Local
		final CyTable localTable = subnet.getTable(type, CyNetwork.LOCAL_ATTRS);
		colNames.addAll(localTable.getColumns().stream().map(col -> col.getName()).collect(Collectors.toList()));
		
		// Hidden
		final CyTable hiddenTable = subnet.getTable(type, CyNetwork.HIDDEN_ATTRS);
		colNames.addAll(hiddenTable.getColumns().stream().map(col -> col.getName()).collect(Collectors.toList()));
		
		return colNames;
	}
	
	private final ArrayList<String> getAllColumnNames(final Class<? extends CyIdentifiable> type) {
		
		final Set<String> colNames = getAllColumnNames(type, _network);

		if (type == CyNetwork.class && _network instanceof CySubNetwork) {
			CyRootNetwork root = ((CySubNetwork) _network).getRootNetwork();
			// Add Root table to available column names
			final CyTable rootTable = root.getDefaultNetworkTable();
			colNames.addAll(rootTable.getColumns().stream().map(col -> col.getName()).collect(Collectors.toList()));
			
			// Add all attributes of sibling networks
			for (CySubNetwork subnet : root.getSubNetworkList()) {
				if (subnet != _network) {
					colNames.addAll(getAllColumnNames(type, subnet));
				}
			}
		}
		
		return new ArrayList<String>(colNames);
	}

	@Override
	public void run(final TaskMonitor monitor) throws FileNotFoundException, IOException {
		if (monitor != null) {
			monitor.setProgress(0.0);
			monitor.setTitle("Exporting to CX");
			monitor.setStatusMessage("Exporting current network as CX...");
		}
		
		final VRNetzExporter exporter = new VRNetzExporter(_network);

		List<String> aspects = aspectFilter.getSelectedValues();

		final long t0 = System.currentTimeMillis();
		if (TimingUtil.WRITE_TO_DEV_NULL) {
			exporter.writeNetwork(aspects, new FileOutputStream(new File("/dev/null")));
		} else if (TimingUtil.WRITE_TO_BYTE_ARRAY_OUTPUTSTREAM) {
			exporter.writeNetwork(aspects, new ByteArrayOutputStream());
		} else {
			exporter.writeNetwork(aspects, _os);
			_os.close();

		}
		
	}

	@Override
	public void cancel() {
		if (_os == null) {
			return;
		}

		try {
			_os.close();
		} catch (final IOException e) {
			System.out.println("Would not closeOutputStream for VRNetzNetworkWriter");
//			monitor.showMessage(TaskMonitor.Level.ERROR, "Writing network table took:"+String.valueOf(totalTime));.error("Could not close Outputstream for CxNetworkWriter.", e);
		}
	}

}