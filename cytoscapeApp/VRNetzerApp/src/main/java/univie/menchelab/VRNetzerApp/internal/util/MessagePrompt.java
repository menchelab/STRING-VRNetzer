package univie.menchelab.VRNetzerApp.internal.util;

import java.io.IOException;
import java.net.URISyntaxException;
import javax.swing.JDialog;
import javax.swing.JEditorPane;
import javax.swing.JScrollPane;
import javax.swing.event.HyperlinkEvent;
import javax.swing.event.HyperlinkListener;
import javax.swing.text.html.HTMLEditorKit;
import org.cytoscape.application.swing.CySwingApplication;



/**
 * Adapted from Cy3d AboutDialog https://github.com/BaderLab/cy3d-impl
 */
@SuppressWarnings("serial")
public class MessagePrompt extends JDialog {

    public MessagePrompt(CySwingApplication application, String content) {
        super(application.getJFrame(), "VRNetzerApp", ModalityType.MODELESS);;

        setResizable(false);

        // main panel for dialog box
        JEditorPane editorPane = new JEditorPane();
        editorPane.setEditable(false);
        editorPane.setEditorKit(new HTMLEditorKit());
        editorPane.addHyperlinkListener(new HyperlinkAction(editorPane));

        editorPane.setText(content);

        JScrollPane scrollPane = new JScrollPane(editorPane);
        setContentPane(scrollPane);

    }

    private class HyperlinkAction implements HyperlinkListener {
        @SuppressWarnings("unused")
        JEditorPane pane;

        public HyperlinkAction(JEditorPane pane) {
            this.pane = pane;
        }

        public void hyperlinkUpdate(HyperlinkEvent event) {
            if (event.getEventType() == HyperlinkEvent.EventType.ACTIVATED) {
                System.out.println("Opening URL: " + event.getURL());
                try {
                    OpenExternalBrowser.browse(event.getURL().toString());
                } catch (IOException | URISyntaxException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
