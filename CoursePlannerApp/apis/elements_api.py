import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.element import Element

bp = Blueprint("elements_api", __name__, url_prefix="/api/v1/elements")
dtb = LocalProxy(get_db)


@bp.route("", methods=["GET"])
def get_elements():
    page = int(request.args.get("page") or 1)

    try:
        elements, prev_page, next_page, count = dtb.get_elements_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    next = url_for("elements_api.get_elements", page=next_page) if next_page else None
    prev = url_for("elements_api.get_elements", page=prev_page) if prev_page else None

    json = {"count": count, "next": next, "prev": prev,
            "results": [element.__dict__ for element in elements]}

    return jsonify(json), 200


@bp.route("/<string:id>", methods=["GET"])
def get_element(id):
    try:
        element = dtb.get_specific_element(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not element:
        return jsonify({"error": "Element not found"}), 404

    return jsonify(element.__dict__), 200


@bp.route("", methods=["POST"])
def add_element():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not all(key in request.json for key in ["id", "order", "name", "criteria", "competency_id"]):
        return jsonify({"error": "Missing fields"}), 400

    element = Element(int(request.json["id"]), int(request.json["order"]), request.json["name"], request.json["criteria"],
                      request.json["competency_id"])

    try:
        dtb.add_element(element)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    resp = make_response({}, 201)
    resp.headers["Location"] = url_for("elements_api.get_element", id=element.id)

    return resp


@bp.route("/<string:id>", methods=["PATCH"])
def update_element(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not all(key in request.json for key in ["order", "name", "criteria", "competency_id"]):
        return jsonify({"error": "Missing fields"}), 400

    element = Element(int(id), int(request.json["order"]), request.json["name"], request.json["criteria"],
                      request.json["competency_id"])

    try:
        dtb.update_element(element)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({}), 204


@bp.route("/<string:id>", methods=["DELETE"])
def delete_element(id):
    try:
        # Just take the id
        dtb.delete_element(Element(int(id), 0, "", "", ""))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({}), 204
