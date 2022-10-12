package univie.menchelab.VRNetzerApp.internal.util;

import java.util.Map;
import java.util.HashMap;
import java.util.List;
import org.cytoscape.model.CyRow;

public class Utility{
//	iterate through all columns and save data in the HashMap
// Generate a new HashMap for Data of node/edge
	public HashMap<String,Object> writeData(HashMap<String,Object> data,Object[] columnsArray, CyRow row, List<String> skipColumns){
		for(int j=0; j< columnsArray.length;j++) {
			 String key = columnsArray[j].toString(); // Name of the Column
			 Object value = row.getRaw(columnsArray[j].toString()); // Value of the Column
			 boolean skip = false;
			 for(String col: skipColumns) {
				 if (key.equals(col)) {
					 skip = true;
					 break;
				 }
			 }
			 if (value != null & !skip) {
				 data.put(key.replace("::", "_"), value); // Remove weird :: characters from column names
			 }
		}
		return data;
	}
	
	public void printMap(Map<String,Object> map) {
	for (Map.Entry<String, Object> entry : map.entrySet()) {
	    String thisEntry = entry.getKey();
	    Map<String,Object> data = (Map<String,Object>) entry.getValue();
	    String k = "";
		String v= "";
		System.out.println(thisEntry);
	    for (Map.Entry<String, Object> dataPoint : data.entrySet()) {
	    	k = dataPoint.getKey();
	    	v = dataPoint.getValue().toString();
		    System.out.printf("\t%s = %s\n", k, v);
	    }
	    System.out.println("");
	}
	}


}