from flask import Flask
from flask_socketio import SocketIO

import string_commands as scmd
import vrnetzer_commands as vcmd
import workflows as workf
from cytoscape_parser import CytoscapeParser
from src.workflows import (call_compound_query, call_disease_query,
                           call_protein_query, call_pubmed_query)

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
        "protein": call_protein_query,
        "disease": call_disease_query,
        "compound": call_compound_query,
        "pubmed": call_pubmed_query,
    }
    # define namespace for query variable
    query_namespace = {}
    for name in ["protein", "disease"]:
        query_namespace[name] = "query"
    query_namespace["disease"] = "disease"
    query_namespace["pubmed"] = "pubmed"
    variable_namespace = {
        "network_type":"networkType",
    }

    parser = CytoscapeParser()
    
    # parse arguments
    arguments = [query, network_type, cutoff, limit, species, taxonID]
    args = [arg for arg in arguments if arg is not None]
    for i,arg in enumerate(args):
        keyword = __dict__.items()
        args[i] = 

    modes[mode](
        parser,
    )
