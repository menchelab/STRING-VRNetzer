package univie.menchelab.VRNetzerApp.internal.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;


public class ConstructJson {
	private String filename;
	public ConstructJson(String filename) {
		this.filename = filename;
	};
	@SuppressWarnings("unchecked")
	public JSONObject generateObject(String header,List<HashMap<String, Object>> data) {
		JSONObject objectToWrite = new JSONObject();
		objectToWrite.put(header, data);
//	    objectToWrite.put("data_type", header); 	//Not needed and causes trouble
//	    objectToWrite.put("amount", data.size());	//Not needed and causes trouble
	    return objectToWrite;
	};
	public void writeObject(JSONObject myObject) throws IOException {
	    Files.write(Paths.get(filename), 
	    		myObject.toJSONString().getBytes());
	    System.out.println(Paths.get(filename));
	};
};
