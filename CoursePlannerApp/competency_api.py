from flask import Blueprint, jsonify
from .dbmanager import get_db

bp = Blueprint('competency_api', __name__, url_prefix='/api/competencies/')

#Competency Page 
@bp.route("/", methods=['GET', 'POST'])
def competencies_api():
    competencies = get_db().get_competencies()
    #Return * competencies in json format
    json = [competency.__dict__ for competency in competencies]
    return jsonify(json)
