package univie.menchelab.VRNetzerApp.internal.util;

import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.BoundedFloat;
import org.cytoscape.work.util.BoundedInteger;

public class UMAPContext {
        final static String N_DESC =
                        "Defines the number of neighbors variable of catoGRAPHs' UMAP algorithms.";
        @Tunable(description = "Number of neighbors",
                        groups = {"VRNetzer variables", "Layout", "Parameters", "UMAP"},
                        params = "displayState=collapsed", tooltip = N_DESC,
                        longDescription = N_DESC, gravity = 4)
        public BoundedInteger neighbors = new BoundedInteger(0, 15, 100, false, false);

        final static String S_DESC = "Defines the spraed variable of catoGRAPHs' UMAP algorithms.";
        @Tunable(description = "Spread",
                        groups = {"VRNetzer variables", "Layout", "Parameters", "UMAP"},
                        params = "displayState=collapsed", tooltip = S_DESC,
                        longDescription = S_DESC, gravity = 5, format = Utility.FLOAT_FORMAT)
        public BoundedFloat spread = new BoundedFloat(0F, 1F, 10F, false, false);

        final static String M_DESC = "Defines the minDist variable of catoGRAPHs' UMAP algorithms.";
        @Tunable(description = "MinDist",
                        groups = {"VRNetzer variables", "Layout", "Parameters", "UMAP"},
                        params = "displayState=collapsed", tooltip = M_DESC,
                        longDescription = M_DESC, gravity = 6, format = Utility.FLOAT_FORMAT)
        public BoundedFloat minDist = new BoundedFloat(0F, 0.1F, 1F, false, false);


}
