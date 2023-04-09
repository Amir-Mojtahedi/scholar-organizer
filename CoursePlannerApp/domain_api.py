from flask import Blueprint, jsonify, request, abort, flash
from .dbmanager import get_db
from .domain import Domain

bp = Blueprint('domain_api', __name__, url_prefix='/api/domains/')

#Competency Page 
@bp.route("/", methods=['GET', 'POST'])
def domain_api():
    domains = get_db().get_domains()
    #Return * domains in json format
    json = [domain.__dict__ for domain in domains]
    return jsonify(json)
