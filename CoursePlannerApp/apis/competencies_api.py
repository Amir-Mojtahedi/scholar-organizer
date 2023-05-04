import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.competency import Competency

bp = Blueprint("competencies_api", __name__, url_prefix="/api/v1/competencies")
dtb = LocalProxy(get_db)


@bp.route("", methods=["GET"])
def get_competencies():
    page = int(request.args.get("page") or 1)

    try:
        competencies, prev_page, next_page, count = dtb.get_competencies_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    next = url_for("competencies_api.get_competencies", page=next_page) if next_page else None
    prev = url_for("competencies_api.get_competencies", page=prev_page) if prev_page else None

    json = {"count": count, "next": next, "prev": prev,
            "results": [competency.__dict__ for competency in competencies]}

    return jsonify(json), 200


@bp.route("/<string:id>", methods=["GET"])
def get_competency(id):
    try:
        competency = dtb.get_specific_competency(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not competency:
        return jsonify({"error": "Competency not found"}), 404

    # insert elements
    try:
        elements = dtb.get_competency_elements(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    competency.elements = [url_for("elements_api.get_element", id=element.id) for element in elements]

    return jsonify(competency.__dict__), 200


@bp.route("", methods=["POST"])
def add_competency():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not all(key in request.json for key in ["id", "name", "achievement", "type"]):
        return jsonify({"error": "Missing fields"}), 400

    competency = Competency(request.json["id"], request.json["name"], request.json["achievement"], request.json["type"])

    try:
        dtb.add_competency(competency)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    resp = make_response({}, 201)
    resp.headers["Location"] = url_for("competencies_api.get_competency", id=competency.id)

    return resp


@bp.route("/<string:id>", methods=["PATCH"])
def update_competency(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not any(key in request.json for key in ["name", "achievement", "type"]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        dtb.update_competency(
            Competency(id, request.json.get("name"), request.json.get("achievement"), request.json.get("type")))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({}), 204


@bp.route("/<string:id>", methods=["DELETE"])
def delete_competency(id):
    try:
        dtb.delete_competency(Competency(id, "", "", ""))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({}), 204
