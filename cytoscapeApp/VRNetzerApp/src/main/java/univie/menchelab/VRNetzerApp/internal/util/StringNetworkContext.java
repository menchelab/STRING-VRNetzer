package univie.menchelab.VRNetzerApp.internal.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Set;
import org.cytoscape.model.CyColumn;
import org.cytoscape.model.CyNetwork;
import org.cytoscape.model.CyRow;
import org.cytoscape.model.CyTable;
import org.cytoscape.model.CyTableManager;
import org.cytoscape.service.util.CyServiceRegistrar;
import org.cytoscape.work.Tunable;
import org.cytoscape.work.util.ListMultipleSelection;
import org.json.simple.JSONObject;

public class StringNetworkContext {

    final String ENRICHMENT_DESC = "Select the table columns which should be exported.";
    @Tunable(description = "Enrichment attributes for export.", tooltip = ENRICHMENT_DESC,
            longDescription = ENRICHMENT_DESC, groups = {"Data tables", "STRING Enrichment"},
            params = "displayState=collapsed")
    public ListMultipleSelection<String> enrichmentAtrributeList = null;


    final String PUBLICATION_DESC = "Select the table columns which should be exported.";
    @Tunable(description = "Publications attributes for export.", tooltip = PUBLICATION_DESC,
            longDescription = PUBLICATION_DESC, groups = {"Data tables", "STRING Enrichment"})
    public ListMultipleSelection<String> publicationAtrrributeList = null;


    List<String> slectedEnrichmentAttributes, selectedPublciationAtrributes = null;

    public List<String> skipEnrichmentColumns =
            new ArrayList<String>(Arrays.asList("nodes.SUID", "network.SUID"));

    public List<String> skipPublicationColumns = new ArrayList<String>(skipEnrichmentColumns);

    public List<String> HideEnrichmentColumns = new ArrayList<String>(skipEnrichmentColumns);
    public List<String> HidePublicationColumns = new ArrayList<String>(skipPublicationColumns);

    public CyTable enrichmentTable = null;
    public CyTable publicationTable = null;

    public StringNetworkContext() {

    }

    public void setup(CyNetwork network, CyServiceRegistrar registrar) {
        CyTableManager tableManager = registrar.getService(CyTableManager.class);
        Set<CyTable> tables = tableManager.getAllTables(true);

        String tableTitle = "";
        for (CyTable table : tables) {
            tableTitle = table.getTitle();

            if (tableTitle.equals("STRING Enrichment: All")) {
                if (table.getColumn("network.SUID") != null) {
                    if (table.getAllRows().size() > 0) {

                        CyRow tempRow = table.getAllRows().get(0);

                        if (tempRow.get("network.SUID", Long.class) != null) {

                            if (tempRow.get("network.SUID", Long.class).equals(network.getSUID())) {

                                enrichmentTable = table;
                            }

                        }
                    }
                }
            } else if (tableTitle.contains("PMID")) {
                if (table.getColumn("network.SUID") != null) {
                    if (table.getAllRows().size() > 0) {
                        CyRow tempRow = table.getAllRows().get(0);
                        if (tempRow.get("network.SUID", Long.class) != null && tempRow
                                .get("network.SUID", Long.class).equals(network.getSUID())) {
                            publicationTable = table;
                        }
                    }
                }
            }
        }
        if (enrichmentTable != null) {
            enrichmentAtrributeList = NetworkUtil.updateEnrichments(network,
                    enrichmentAtrributeList, "STRING Enrichment", HideEnrichmentColumns, registrar);
            if (enrichmentAtrributeList != null) {
                slectedEnrichmentAttributes = enrichmentAtrributeList.getSelectedValues();
                skipEnrichmentColumns.addAll(Utility.getFilteredList(enrichmentAtrributeList,
                        slectedEnrichmentAttributes));
            }
        }
        if (publicationTable != null) {

            publicationAtrrributeList = NetworkUtil.updateEnrichments(network,
                    enrichmentAtrributeList, "PMID", HidePublicationColumns, registrar);

            if (publicationAtrrributeList != null) {
                selectedPublciationAtrributes = publicationAtrrributeList.getSelectedValues();
                skipPublicationColumns.addAll(Utility.getFilteredList(
                        this.publicationAtrrributeList, selectedPublciationAtrributes));
            }
        }

    }

    @SuppressWarnings("unchecked")
    public JSONObject extractEnrichmentTables(JSONObject networkJson,
            CyServiceRegistrar registrar) {
        if (enrichmentTable != null)
            networkJson.put("enrichment",
                    getEnrichmentData(enrichmentTable, skipEnrichmentColumns));
        if (publicationTable != null)
            networkJson.put("publications",
                    getEnrichmentData(publicationTable, skipPublicationColumns));
        return networkJson;
    }

    public List<HashMap<String, Object>> getEnrichmentData(CyTable table, List<String> skip) {
        System.out.println("Table name: " + table.getTitle());
        List<HashMap<String, Object>> mapList = new ArrayList<HashMap<String, Object>>();
        List<CyRow> rows = table.getAllRows();
        Collection<CyColumn> columns = table.getColumns();
        Object[] columnsArray = columns.toArray();

        // System.out.println(rows.size());
        for (int i = 0; i < rows.size(); i++) {
            HashMap<String, Object> data = new HashMap<>();
            CyRow row = rows.get(i);
            data = Utility.writeData(data, columnsArray, row, skip);
            mapList.add(data);
        }
        return (List<HashMap<String, Object>>) mapList;

    }


}
