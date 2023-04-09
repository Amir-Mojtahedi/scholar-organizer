from flask import Blueprint, jsonify
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.element import Element

bp = Blueprint('element_api', __name__, url_prefix='/api/elements/')

#Element Page 
@bp.route("/", methods=['GET', 'POST'])
def elements_api():
    elements = get_db().get_elements()
    #Return * elements in json format
    json = [element.__dict__ for element in elements]
    return jsonify(json)
