package univie.menchelab.VRNetzerApp.internal.util;

import java.util.Collection;
import java.util.HashMap;
import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.ListSingleSelection;

public class AlgorithmContext {

        public HashMap<String, Object> parameters = new HashMap<String, Object>();
        public String layoutName = "spring";
        public ListSingleSelection<String> algorithm = new ListSingleSelection<String>("spring",
                        "kamada-kawai", "cartoGRAPHs local umap", "cartoGRAPHs global umap",
                        "cartoGRAPHs local tsne", "cartoGRAPHs global tsne",
                        "cartoGRAPHs importance umap", "cartoGRAPHs importance tsne");


        @Tunable(description = "Layout Algorithm", groups = {"VRNetzer variables", "Layout"},
                        params = "groupdTitles=displayed, displayed", gravity = 0)
        public ListSingleSelection<String> getAlgorithm() {
                return algorithm;
        }

        public void setAlgorithm(ListSingleSelection<String> algorithm) {
                this.algorithm = algorithm;
        }

        @Tunable(description = "Layout Name", required = true, exampleStringValue = "spring",
                        groups = {"VRNetzer variables", "Layout"}, listenForChange = "Algorithm",
                        gravity = 1)
        public String getLayoutName() {
                Collection<String> algo = getMap().values();
                if (algo.contains(layoutName) || layoutName == "") {
                        return getMap().get(algorithm.getSelectedValue());
                } else {
                        return layoutName.replace(" ", "_");
                }
        }

        public void setLayoutName(String layoutName) {
                this.layoutName = layoutName;
        }


        public String selectedLayout() {
                return getMap().get(algorithm.getSelectedValue());
        }

        public HashMap<String, String> getMap() {
                HashMap<String, String> layout = new HashMap<String, String>();
                layout.put("spring", "spring");
                layout.put("kamada-kawai", "kamada_kawai");
                layout.put("cartoGRAPHs local umap", "cg_local_umap");
                layout.put("cartoGRAPHs global umap", "cg_global_umap");
                layout.put("cartoGRAPHs local tsne", "cg_local_tsne");
                layout.put("cartoGRAPHs global tsne", "cg_global_tsne");
                layout.put("cartoGRAPHs importance umap", "cg_importance_umap");
                layout.put("cartoGRAPHs importance tsne", "cg_importance_tsne");
                return layout;
        }
}
