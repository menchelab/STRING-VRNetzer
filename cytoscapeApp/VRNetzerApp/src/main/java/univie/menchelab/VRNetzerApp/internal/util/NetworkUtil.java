package univie.menchelab.VRNetzerApp.internal.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.cytoscape.model.CyColumn;
import org.cytoscape.model.CyIdentifiable;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyTable;
import org.cytoscape.work.util.ListMultipleSelection;

public class NetworkUtil {


	public static ListMultipleSelection<String> updateNodeEdgeAttributeList(CyNetwork network,
			ListMultipleSelection<String> attribute, Class<? extends CyIdentifiable> edgeNode,
			List<String> skipColumns) {
		if (network == null)
			return new ListMultipleSelection<String>();
		List<String> attributeArray = getAllAttributes(network,
				network.getTable(edgeNode, CyNetwork.LOCAL_ATTRS), skipColumns);

		if (attributeArray.size() > 0) {
			ListMultipleSelection<String> newAttribute =
					new ListMultipleSelection<String>(attributeArray);
			if (attribute != null) {
				try {
					newAttribute.setSelectedValues(newAttribute.getPossibleValues());
				} catch (IllegalArgumentException e) {
					newAttribute
							.setSelectedValues(Collections.singletonList(attributeArray.get(0)));
				}
			} else
				newAttribute.setSelectedValues(newAttribute.getPossibleValues());

			return newAttribute;
		}
		return new ListMultipleSelection<String>("--None--");
	}

	private static List<String> getAllAttributes(CyNetwork network, CyTable table,
			List<String> skipColumns) {
		String[] attributeArray = new String[1];
		List<String> attributeList = new ArrayList<String>();
		getAttributesList(attributeList, table, skipColumns);
		String[] attrArray = attributeList.toArray(attributeArray);
		if (attrArray.length > 1)
			Arrays.sort(attrArray);
		return Arrays.asList(attrArray);
	}

	private static void getAttributesList(List<String> attributeList, CyTable attributes,
			List<String> skipColumns) {
		if (attributes == null)
			return;

		for (CyColumn column : attributes.getColumns()) {
			String columnName = column.getName();
			if (!skipColumns.contains(columnName)) {
				attributeList.add(column.getName());
			}
		}
	}


}


