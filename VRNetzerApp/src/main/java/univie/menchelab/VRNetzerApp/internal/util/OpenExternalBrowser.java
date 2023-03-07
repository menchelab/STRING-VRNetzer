package univie.menchelab.VRNetzerApp.internal.util;


import java.awt.Desktop;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

/*
 * Adapted from CyRest https://github.com/cytoscape/cyREST
 */
public class OpenExternalBrowser {
    public static void browse(String url) throws IOException, URISyntaxException {
        URI uri = null;
        uri = new URI(url);
        Desktop.getDesktop().browse(uri);
    }
}
