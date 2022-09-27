#! python3

import sys

import argumentparser as ap
from cytoscape_parser import CytoscapeParser
from settings import HELP_TEXT


def main():
    """Guides the user through the workflows."""

    if len(sys.argv) == 1:
        print(HELP_TEXT)
        return
    keyword = sys.argv[1]
    if keyword in ["query", "export", "names"]:
        cparser = CytoscapeParser()
        if keyword == "query":
            ap.call_query_workflow(cparser)
        elif keyword == "names":
            ap.print_networks_workflow(cparser)
        elif keyword == "export":
            ap.call_export_workflow(cparser)
    elif keyword == "project":
        ap.call_create_project_workflow()
    elif keyword == "map":
        ap.call_map_workflow()
    elif keyword == "convert":
        ap.call_convert()


if __name__ == "__main__":
    main()
