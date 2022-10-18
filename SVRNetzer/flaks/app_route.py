from flask import Flask
from flask_socketio import SocketIO

from ..util import string_commands as scmd
from ..util import vrnetzer_commands as vcmd
from ..util.cytoscape_parser import CytoscapeParser
from ..util import workflows as wf

app = Flask(__name__)
app.debug = False
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_TYPE"] = "filesystem"


socketio = SocketIO(app, manage_session=False)


@app.route(
    "/String/fetch/<mode>_<query>_<network_type>_<cutoff>_<limit>_<species>_<taxon>",
    methods=["Get"],
)
def fetch_string_network(mode, query, network_type, cutoff, limit, species, taxonID):
    """Fetches the a network using the StringApp in Cytoscape. This network will then be exported to a .VRNetz file. It is used to generate the VRNetzer project and can than be presented to the viewer."""
    modes = {
        "protein": wf.call_protein_query,
        "disease": wf.call_disease_query,
        "compound": wf.call_compound_query,
        "pubmed": wf.call_pubmed_query,
    }
    # define namespace for query variable
    query_namespace = {}
    for name in ["protein", "disease"]:
        query_namespace[name] = "query"
    query_namespace["disease"] = "disease"
    query_namespace["pubmed"] = "pubmed"
    variable_namespace = {
        "network_type": "networkType",
    }

    parser = CytoscapeParser()

    # parse arguments
    arguments = [query, network_type, cutoff, limit, species, taxonID]
    args = [arg for arg in arguments if arg is not None]
    for i, arg in enumerate(args):
        keyword = __dict__.items()
        args[i] = 2

    modes[mode](
        parser,
    )
