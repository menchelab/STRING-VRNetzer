package univie.menchelab.VRNetzerApp.internal.util;

import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.BoundedFloat;
import org.cytoscape.work.util.BoundedInteger;

public class SpringContext {

    final static String OD_DESC =
            "Defines the parameter k of NetworkX's spring layout algorithm. If this value is 0.0 default value k = 1/sqrt(n) is used.";

    @Tunable(description = "Optimal distance",
            groups = {"VRNetzer variables", "Layout", "Parameters", "Spring"},
            params = "displayState=collapsed", longDescription = OD_DESC, tooltip = OD_DESC,
            format = Utility.FLOAT_FORMAT, gravity = 3)
    public BoundedFloat optDist = new BoundedFloat(0.0F, 0.0F, 1.0F, false, false);

    final static String IT_DESC =
            "Defines the iterations parameter of NetworkX's spring layout algorithm.";

    @Tunable(description = "Iterations",
            groups = {"VRNetzer variables", "Layout", "Parameters", "Spring"},
            params = "displayState=collapsed", longDescription = IT_DESC, tooltip = IT_DESC,
            gravity = 3)
    public BoundedInteger iter = new BoundedInteger(0, 50, 100, false, false);

    final static String THR_DESC =
            "Defines the threshold parameter of NetworkX's spring layout algorithm.";
    @Tunable(description = "Threshold",
            groups = {"VRNetzer variables", "Layout", "Parameters", "Spring"},
            params = "displayState=collapsed", longDescription = IT_DESC, tooltip = IT_DESC,
            format = Utility.FLOAT_FORMAT, gravity = 3)
    public BoundedFloat thresh = new BoundedFloat(0F, 0.0001F, 1F, false, false);

}
