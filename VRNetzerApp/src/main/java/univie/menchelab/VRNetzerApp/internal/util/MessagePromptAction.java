package univie.menchelab.VRNetzerApp.internal.util;


import java.awt.event.ActionEvent;
import javax.swing.JDialog;
import org.cytoscape.application.swing.AbstractCyAction;
import org.cytoscape.application.swing.CySwingApplication;
import org.cytoscape.service.util.CyServiceRegistrar;

/**
 * Adapted from Cy3d AboutDialog https://github.com/BaderLab/cy3d-impl
 */
@SuppressWarnings("serial")
public class MessagePromptAction extends AbstractCyAction {

	private CySwingApplication application;
	private String content;

	public MessagePromptAction(CyServiceRegistrar registrar, String content) {
		super("VRNetzerApp");
		this.application = registrar.getService(CySwingApplication.class);
		this.content = content;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		JDialog aboutDialog = new MessagePrompt(application, content);
		aboutDialog.pack();
		aboutDialog.setLocationRelativeTo(application.getJFrame());
		aboutDialog.setVisible(true);
	}

}
