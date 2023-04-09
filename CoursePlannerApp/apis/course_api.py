from flask import Blueprint, jsonify, request, abort, flash
from ..dbmanager import get_db
from ..objects.course import Course

bp = Blueprint('course_api', __name__, url_prefix='/api/courses/')

#Competency Page 
@bp.route("/", methods=['GET', 'POST'])
def course_api():
    courses = get_db().get_courses()
    #Return * courses in json format
    json = [course.__dict__ for course in courses]
    return jsonify(json)
