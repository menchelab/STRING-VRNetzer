package univie.menchelab.VRNetzerApp.internal.util;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyNetworkManager;
import org.cytoscape.model.CyRow;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.view.model.CyNetworkView;
import org.cytoscape.view.model.CyNetworkViewManager;
import org.cytoscape.work.util.ListMultipleSelection;

public class Utility {

	public final static String FLOAT_FORMAT = "#.#########";

	// iterate through all columns and save data in the HashMap
	// Generate a new HashMap for Data of node/edge
	@SuppressWarnings("unchecked")
	public static HashMap<String, Object> writeData(HashMap<String, Object> data,
			Object[] columnsArray, CyRow row, List<String> skipColumns) {
		for (int j = 0; j < columnsArray.length; j++) {
			String key = columnsArray[j].toString(); // Name of the Column
			Object value = row.getRaw(columnsArray[j].toString()); // Value of the Column
			if (value == null)
				continue;
			// ignore defined column
			if (skipColumns.contains(key))
				continue;

			if (key.equals("display name"))
				data.put("n", value);

			if (key.equals("stringdb::canonical name")) {
				List<String> uniprot = new ArrayList<String>();
				uniprot.add(value.toString());
				data.put("uniprot", uniprot);
			} ;


			// ignore empty values
			if (value instanceof String) {
				if (value.equals(""))
					continue;

			} ;
			// ignore stringdb_structures, if there is no structure listed
			if (key.equals("stringdb::structures")) {
				List<String> structures = (List<String>) value;
				// System.out.println(structures.size());
				if (structures.size() == 1) {
					if (structures.get(0).equals(""))
						continue;
				} ;
			} ;
			data.put(key.replace("::", "_"), value); // Remove weird :: characters from column names
		} ;
		return data;
	};

	@SuppressWarnings("unchecked")
	public void printMap(Map<String, Object> map) {
		for (Map.Entry<String, Object> entry : map.entrySet()) {
			String thisEntry = entry.getKey();
			Map<String, Object> data = (Map<String, Object>) entry.getValue();
			String k = "";
			String v = "";
			// System.out.println(thisEntry);
			for (Map.Entry<String, Object> dataPoint : data.entrySet()) {
				k = dataPoint.getKey();
				v = dataPoint.getValue().toString();
				// System.out.printf("\t%s = %s\n", k, v);
			} ;
			// System.out.println("");
		} ;
	};

	public static void validate(CyNetwork network, CyNetworkView netView,
			CyServiceRegistrar registrar) {
		// Get current network
		if (network == null) {
			CyNetworkManager netMgr = registrar.getService(CyNetworkManager.class);
			Set<CyNetwork> networks = netMgr.getNetworkSet();
			if (networks.isEmpty()) {
				throw new RuntimeException("No network to export!");
			}
			network = networks.iterator().next();
		}

		if (netView == null) {
			Collection<CyNetworkView> views =
					registrar.getService(CyNetworkViewManager.class).getNetworkViews(network);
			if (views.isEmpty()) {
				throw new RuntimeException("You first have to create a network view!");
			}
		}
	}

	public static List<String> getFilteredList(ListMultipleSelection<String> list,
			List<String> selected) {
		List<String> skipColumns = new ArrayList<String>();
		for (String attr : list.getPossibleValues()) {
			if (!selected.contains(attr)) {
				skipColumns.add(attr);
			}
		}
		return skipColumns;
	}
};
