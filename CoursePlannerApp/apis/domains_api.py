import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.domain import Domain

bp = Blueprint("domains_api", __name__, url_prefix="/api/v1/domains")
dtb = LocalProxy(get_db)


@bp.route("", methods=["GET"])
def get_domains():
    page = int(request.args.get("page") or 1)

    try:
        domains, prev_page, next_page, count = dtb.get_domains_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    next = url_for("domains_api.get_domains", page=next_page) if next_page else None
    prev = url_for("domains_api.get_domains", page=prev_page) if prev_page else None

    json = {"count": count, "next": next, "prev": prev,
            "results": [domain.__dict__ for domain in domains]}

    return jsonify(json), 200


@bp.route("/<int:id>", methods=["GET"])
def get_domain(id):
    try:
        domain = dtb.get_specific_domain(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not domain:
        return jsonify({"error": "Domain not found"}), 404

    return jsonify(domain.__dict__), 200


@bp.route("", methods=["POST"])
def add_domain():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "id" not in request.json or "name" not in request.json or "description" not in request.json:
        return jsonify({"error": "Missing data to add"}), 400

    id = request.json["id"]
    name = request.json["name"]
    description = request.json["description"]

    try:
        dtb.add_domain(Domain(id, name, description))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    res = make_response({}, 201)
    res.headers['Location'] = url_for("domains_api.get_domain", id=id)

    return res


@bp.route("/<int:id>", methods=["PATCH"])
def update_domain(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in request.json and "description" not in request.json:
        return jsonify({"error": "Missing data to update"}), 400

    name = request.json.get("name")
    description = request.json.get("description")

    try:
        dtb.update_domain(id, name, description)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204


@bp.route("/<int:id>", methods=["DELETE"])
def delete_domain(id):
    try:
        dtb.delete_domain(Domain(id, "", ""))
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204
