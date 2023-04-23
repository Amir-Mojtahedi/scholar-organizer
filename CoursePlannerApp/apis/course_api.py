from flask import Blueprint, jsonify
from werkzeug.local import LocalProxy
import oracledb

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.course import Course


bp = Blueprint('courses_api', __name__, url_prefix='/api/courses/')

dtb = LocalProxy(get_db)

#Delete Course
@bp.route("/<course_id>/", methods=["DELETE"])
def delete_course(course_id):
    # get course
    try:
        course = dtb.get_course(course_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not course:
        return jsonify({"error": "Course not found"}), 404

    # delete Course
    try:
        dtb.delete_course(course)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200