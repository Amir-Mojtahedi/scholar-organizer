import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.element import Element

bp = Blueprint("elements_api", __name__, url_prefix="/api/v1/elements")
dtb = LocalProxy(get_db)


@bp.route("")
def get_elements():
    # pagination
    page = int(request.args.get("page") or 1)

    # get elements
    try:
        elements, prev_page, next_page, count = dtb.get_elements_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    # pagination urls
    next = url_for(".get_elements", page=next_page) if next_page else None
    prev = url_for(".get_elements", page=prev_page) if prev_page else None

    # add self url to elements
    for element in elements:
        element.url = url_for(".get_element", id=element.id)

    # structure json
    json = {"count": count, "next": next, "prev": prev,
            "results": [element.__dict__ for element in elements]}

    # return json
    return jsonify(json), 200


@bp.route("/<string:id>")
def get_element(id):
    try:
        element = dtb.get_element(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not element:
        return jsonify({"error": "Element not found"}), 404

    element.url = url_for(".get_element", id=element.id)

    return jsonify(element.__dict__), 200


@bp.route("", methods=["POST"])
def add_element():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not all(key in request.json for key in ["id", "order", "name", "criteria", "competency_id"]):
        return jsonify({"error": "Missing fields"}), 400

    element = Element(request.json["id"], request.json["order"], request.json["name"], request.json["criteria"],
                      request.json["competency_id"])

    try:
        dtb.add_element(element)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    resp = make_response({}, 201)
    resp.headers["Location"] = url_for(".get_element", id=element.id)

    return resp


@bp.route("/<string:id>", methods=["PUT"])
def update_element(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if not all(key in request.json for key in ["order", "name", "criteria", "competency_id"]):
        return jsonify({"error": "Missing fields"}), 400

    element = Element(id, request.json["order"], request.json["name"], request.json["criteria"],
                      request.json["competency_id"])

    try:
        dtb.update_element(element)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except KeyError:  # raised manually when term not found
        try:
            dtb.add_element(element)
        except oracledb.Error as e:
            return jsonify({"error": str(e)}), 500

        res = make_response({}, 201)
        res.headers["Location"] = url_for(".get_element", id=element.id)

        return res

    return {}, 204


@bp.route("/<string:id>", methods=["DELETE"])
def delete_element(id):
    try:
        dtb.delete_element(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204
