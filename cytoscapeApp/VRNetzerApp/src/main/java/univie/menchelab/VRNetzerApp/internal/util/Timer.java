package univie.menchelab.VRNetzerApp.internal.util;

import org.cytoscape.work.TaskMonitor;
import org.cytoscape.work.TaskMonitor.Level;

public class Timer {

	private long start = 0;
	private String message = "";
	private TaskMonitor monitor;
	private Level level = null;

	public Timer(String message, TaskMonitor monitor, Level level) {
		this.message = message;
		this.monitor = monitor;
		this.level = level;
	}

	public void start() {
		this.start = System.nanoTime();
	}

	public void stop() {
		final long totalTime = System.nanoTime() - this.start;
		final double totalTimeInSeconds = (double) totalTime / 1_000_000_000;
		monitor.showMessage(this.level, message + "Runtime:" + String.valueOf(totalTimeInSeconds));
	}
}
