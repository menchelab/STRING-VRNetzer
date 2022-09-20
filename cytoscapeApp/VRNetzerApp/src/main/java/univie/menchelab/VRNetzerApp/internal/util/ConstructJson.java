package univie.menchelab.VRNetzerApp.internal.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;


public class ConstructJson {
	private String filename;
	public ConstructJson(String filename) {
		this.filename = filename;
	}
	public JSONObject generateObject(String header,Map<String,Object> data) {
		JSONObject objectToWrite = new JSONObject();
		objectToWrite.putAll(data);
//	    objectToWrite.put("data_type", header); 	//Not needed and causes trouble
//	    objectToWrite.put("amount", data.size());	//Not needed and causes trouble
	    return objectToWrite;
	}
	public void writeObject(JSONObject myObject) throws IOException {
	    Files.write(Paths.get(filename), 
	    		myObject.toJSONString().getBytes());
	    System.out.println(Paths.get(filename));
	}
}
