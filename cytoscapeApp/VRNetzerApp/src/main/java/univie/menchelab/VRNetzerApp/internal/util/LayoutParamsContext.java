package univie.menchelab.VRNetzerApp.internal.util;

import org.cytoscape.work.ContainsTunables;

public class LayoutParamsContext {

    @ContainsTunables
    public SpringContext springContext = null;

    @ContainsTunables
    public UMAPContext umapContext = null;

    @ContainsTunables
    public TSNEContext tsneContext = null;

    public LayoutParamsContext(SpringContext springContext, UMAPContext umapContext,
            TSNEContext tsneContext) {
        this.springContext = springContext;
        this.umapContext = umapContext;
        this.tsneContext = tsneContext;
    }

}
