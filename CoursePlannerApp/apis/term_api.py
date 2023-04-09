from flask import Blueprint, jsonify, request, abort, flash
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.term import Term

bp = Blueprint('term_api', __name__, url_prefix='/api/terms/')

#Competency Page 
@bp.route("/", methods=['GET', 'POST'])
def term_api():
    terms = get_db().get_terms()
    #Return * terms in json format
    json = [term.__dict__ for term in terms]
    return jsonify(json)
