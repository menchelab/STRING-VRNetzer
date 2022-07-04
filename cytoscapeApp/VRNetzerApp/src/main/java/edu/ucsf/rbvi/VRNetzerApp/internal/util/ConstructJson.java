package edu.ucsf.rbvi.VRNetzerApp.internal.util;

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
	    objectToWrite.put("data_type", header);
	    objectToWrite.put("ammount", data.size());
	    
	    JSONObject dataJson = new JSONObject();
	    
	    for (Map.Entry<String, Object> entry : data.entrySet()) {
		    String thisEntry = entry.getKey();
		    JSONObject entryObject = new JSONObject();
		    Map<String,Object> entryData = (Map<String,Object>) entry.getValue();
		    entryObject.putAll(entryData);
		    dataJson.put(thisEntry,entryObject);
		}
	    objectToWrite.put("data", dataJson);
	    return objectToWrite;
	}
	public void writeObject(JSONObject myObject) throws IOException {
	    Files.write(Paths.get(filename), 
	    		myObject.toJSONString().getBytes());
	    System.out.println(Paths.get(filename));
	}
}
