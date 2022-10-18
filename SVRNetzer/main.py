#! python3

import sys

from util import argumentparser as ap
from util.cytoscape_parser import CytoscapeParser
from util.settings import HELP_TEXT


def main(arg=sys.argv) -> None:
    """Guides the user through the workflows."""
    if len(arg) == 1:
        print(HELP_TEXT)
        return
    keyword = arg[1]
    if keyword in ["query", "export", "names"]:
        cparser = CytoscapeParser()
        if keyword == "query":
            ap.call_query_workflow(cparser, arg)
        elif keyword == "names":
            ap.print_networks_workflow(cparser)
        elif keyword == "export":
            ap.call_export_workflow(cparser, arg=arg)
    elif keyword == "project":
        ap.call_create_project_workflow(arg)
    elif keyword == "map":
        ap.call_map_workflow(arg)
    elif keyword == "convert":
        ap.call_convert(arg)
        print(keyword)
    else:
        print(HELP_TEXT)
        return


if __name__ == "__main__":
    main()
