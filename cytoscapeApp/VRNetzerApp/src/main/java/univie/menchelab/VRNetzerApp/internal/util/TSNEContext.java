package univie.menchelab.VRNetzerApp.internal.util;

import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.BoundedFloat;
import org.cytoscape.work.util.BoundedInteger;

public class TSNEContext {

        final static String P_DESC =
                        "Defines the perplexity variable of catoGRAPHs' TSNE algorithms.";
        @Tunable(description = "Perplexity",
                        groups = {"VRNetzer variables", "Layout", "Parameters", "TSNE"},
                        params = "displayState=collapsed", tooltip = P_DESC,
                        longDescription = P_DESC, gravity = 7)
        public BoundedInteger prplxty = new BoundedInteger(0, 20, 100, false, false);

        final static String D_DESC = "Defines the density variable of catoGRAPHs' TSNE algorithms.";
        @Tunable(description = "Density",
                        groups = {"VRNetzer variables", "Layout", "Parameters", "TSNE"},
                        params = "displayState=collapsed", tooltip = D_DESC,
                        longDescription = D_DESC, gravity = 8, format = Utility.FLOAT_FORMAT)
        public BoundedFloat density = new BoundedFloat(0F, 12F, 100F, false, false);

        final static String L_DESC =
                        "Defines the learning rate variable of catoGRAPHs' TNSE algorithms.";
        @Tunable(description = "Learning Rate",
                        groups = {"VRNetzer variables", "Layout", "Parameters", "TSNE"},
                        params = "displayState=collapsed", tooltip = L_DESC, gravity = 7,
                        format = Utility.FLOAT_FORMAT, longDescription = L_DESC)
        public BoundedFloat lRate = new BoundedFloat(0F, 200F, 1000F, false, false);

        final static String S_DESC = "Defines the steps variable of catoGRAPHs' TSNE algorithms.";
        @Tunable(description = "Steps",
                        groups = {"VRNetzer variables", "Layout", "Parameters", "TSNE"},
                        params = "displayState=collapsed", tooltip = S_DESC,
                        longDescription = S_DESC, gravity = 9)
        public BoundedInteger steps = new BoundedInteger(0, 250, 10000, false, false);



}
