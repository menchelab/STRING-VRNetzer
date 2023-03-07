package univie.menchelab.VRNetzerApp.internal.util;

import org.cytoscape.work.ContainsTunables;
import org.cytoscape.work.util.ListChangeListener;
import org.cytoscape.work.util.ListSelection;
import org.cytoscape.work.util.ListSingleSelection;

public class UpdateTargetListener<T> implements ListChangeListener<T> {
    @ContainsTunables
    Object classInstance = null;

    @ContainsTunables
    Object targetTunable = null;

    T value = null;

    public UpdateTargetListener(Object target, T value) {
        this.targetTunable = target;
        this.classInstance = targetTunable;
        this.value = value;
    }

    @Override
    public void selectionChanged(ListSelection<T> source) {
        System.out.println("SELCTION CHANGED");
        ListSingleSelection<T> listSelection = (ListSingleSelection<T>) source;
        if (listSelection.getSelectedValue().equals(value)) {
            targetTunable = classInstance;
            System.out.println("Set to" + targetTunable.toString());
        } else {
            targetTunable = null;
            System.out.println("Set to null");
        }

    };

    @Override
    public void listChanged(ListSelection<T> source) {};

}
