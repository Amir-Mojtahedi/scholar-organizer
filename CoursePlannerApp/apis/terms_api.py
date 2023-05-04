import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.term import Term

bp = Blueprint("terms_api", __name__, url_prefix="/api/v1/terms")
dtb = LocalProxy(get_db)


@bp.route("", methods=["GET"])
def get_terms():
    page = int(request.args.get("page") or 1)

    try:
        terms, prev_page, next_page, count = dtb.get_terms_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    next = url_for("terms_api.get_terms", page=next_page) if next_page else None
    prev = url_for("terms_api.get_terms", page=prev_page) if prev_page else None

    json = {"count": count, "next": next, "prev": prev,
            "results": [term.__dict__ for term in terms]}

    return jsonify(json), 200


@bp.route("/<int:id>", methods=["GET"])
def get_term(id):
    try:
        term = dtb.get_specific_term(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not term:
        return jsonify({"error": "Term not found"}), 404

    return jsonify(term.__dict__), 200


@bp.route("", methods=["POST"])
def add_term():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "id" not in request.json or "name" not in request.json:
        return jsonify({"error": "Missing data to add"}), 400

    id = request.json["id"]
    name = request.json["name"]

    try:
        dtb.add_term(Term(id, name))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    res = make_response({}, 201)
    res.headers['Location'] = url_for("terms_api.get_term", id=id)

    return res


@bp.route("/<int:id>", methods=["PATCH"])
def update_term(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in request.json:
        return jsonify({"error": "Missing data to update"}), 400

    name = request.json["name"]

    try:
        dtb.update_term(Term(id, name))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204


@bp.route("/<int:id>", methods=["DELETE"])
def delete_term(id):
    try:
        dtb.delete_term(Term(id, ""))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204