import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.competency import Competency

bp = Blueprint("competencies_api", __name__, url_prefix="/api/v1/competencies")
dtb = LocalProxy(get_db)


@bp.route("")
def get_competencies():
    # pagination
    page = int(request.args.get("page") or 1)

    # get competencies
    try:
        competencies, prev_page, next_page, count = dtb.get_competencies_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    # pagination urls
    next = url_for(".get_competencies", page=next_page) if next_page else None
    prev = url_for(".get_competencies", page=prev_page) if prev_page else None

    # add self url to competencies
    for competency in competencies:
        competency.url = url_for(".get_competency", id=competency.id)

    # structure json
    json = {"count": count, "next": next, "prev": prev,
            "results": [competency.__dict__ for competency in competencies]}

    # return json
    return jsonify(json), 200


@bp.route("/<string:id>")
def get_competency(id):
    try:
        competency = dtb.get_competency(id)
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
    competency.url = url_for(".get_competency", id=competency.id)

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
    resp.headers["Location"] = url_for(".get_competency", id=competency.id)

    return resp


@bp.route("/<string:id>", methods=["PUT"])
def update_competency(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not any(key in request.json for key in ["name", "achievement", "type"]):
        return jsonify({"error": "Missing fields"}), 400

    competency = Competency(id, request.json["name"], request.json["achievement"], request.json["type"])

    try:
        dtb.update_competency(competency)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return {}, 204


@bp.route("/<string:id>", methods=["DELETE"])
def delete_competency(id):
    try:
        dtb.delete_competency(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204
