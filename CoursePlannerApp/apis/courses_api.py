import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.course import Course

bp = Blueprint("courses_api", __name__, url_prefix="/api/v1/courses")
dtb = LocalProxy(get_db)


@bp.route("", methods=["GET"])
def get_courses():
    page = int(request.args.get("page") or 1)

    try:
        courses, prev_page, next_page, count = dtb.get_courses_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    next = url_for("courses_api.get_courses", page=next_page) if next_page else None
    prev = url_for("courses_api.get_courses", page=prev_page) if prev_page else None

    json = {"count": count, "next": next, "prev": prev,
            "results": [course.__dict__ for course in courses]}

    return jsonify(json), 200


@bp.route("/<string:id>", methods=["GET"])
def get_course(id):
    try:
        course = dtb.get_specific_course(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not course:
        return jsonify({"error": "Course not found"}), 404

    # insert competencies and elements
    try:
        competencies = dtb.get_course_competencies(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    try:
        elements = dtb.get_elements_covered_by_a_course(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    course.competencies = [url_for("competencies_api.get_competency", id=competency.id) for competency in competencies]
    course.elements_covered = [url_for("elements_api.get_element", id=element.id) for element in elements]

    return jsonify(course.__dict__), 200


@bp.route("", methods=["POST"])
def add_course():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not all(key in request.json for key in
               ["id", "name", "theory_hours", "lab_hours", "work_hours", "description", "domain_id", "term_id"]):
        return jsonify({"error": "Missing data to add"}), 400

    id = request.json["id"]
    name = request.json["name"]
    theory_hours = request.json["theory_hours"]
    lab_hours = request.json["lab_hours"]
    work_hours = request.json["work_hours"]
    description = request.json["description"]
    domain_id = request.json["domain_id"]
    term_id = request.json["term_id"]

    try:
        dtb.add_course(Course(id=id, name=name, theory_hours=int(theory_hours), lab_hours=int(lab_hours), work_hours=int(work_hours),
                              description=description, domainId=int(domain_id), termId=int(term_id)))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    resp = make_response({}, 201)
    resp.headers["Location"] = url_for("courses_api.get_course", id=id)

    return resp


@bp.route("/<string:id>", methods=["PATCH"])
def update_course(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not all(key in request.json for key in
               ["name", "theory_hours", "lab_hours", "work_hours", "description", "domain_id", "term_id"]):
        return jsonify({"error": "Missing data to update"}), 400

    name = request.json["name"]
    theory_hours = request.json["theory_hours"]
    lab_hours = request.json["lab_hours"]
    work_hours = request.json["work_hours"]
    description = request.json["description"]
    domain_id = request.json["domain_id"]
    term_id = request.json["term_id"]

    try:
        dtb.update_course(Course(id=id, name=name, theory_hours=int(theory_hours), lab_hours=int(lab_hours), work_hours=int(work_hours),
                              description=description, domainId=int(domain_id), termId=int(term_id)))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({}), 204


@bp.route("/<string:id>", methods=["DELETE"])
def delete_course(id):
    try:
        dtb.delete_course(Course(id, "", "", "", "", 0, 0, 0))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({}), 204
