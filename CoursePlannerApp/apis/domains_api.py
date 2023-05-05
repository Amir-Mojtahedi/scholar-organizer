import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.domain import Domain

bp = Blueprint("domains_api", __name__, url_prefix="/api/v1/domains")
dtb = LocalProxy(get_db)


@bp.route("")
def get_domains():
    # pagination
    page = int(request.args.get("page") or 1)

    # get domains
    try:
        domains, prev_page, next_page, count = dtb.get_domains_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    # pagination urls
    next = url_for(".get_domains", page=next_page) if next_page else None
    prev = url_for(".get_domains", page=prev_page) if prev_page else None

    # add self url to domains
    for domain in domains:
        domain.url = url_for(".get_domain", id=domain.id)

    # structure json
    json = {"count": count, "next": next, "prev": prev,
            "results": [domain.__dict__ for domain in domains]}

    # return json
    return jsonify(json), 200


@bp.route("/<int:id>")
def get_domain(id):
    try:
        domain = dtb.get_domain(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not domain:
        return jsonify({"error": "Domain not found"}), 404

    domain.url = url_for(".get_domain", id=domain.id)

    return jsonify(domain.__dict__), 200


@bp.route("", methods=["POST"])
def add_domain():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "id" not in request.json or "name" not in request.json or "description" not in request.json:
        return jsonify({"error": "Missing data to add"}), 400

    domain = Domain(request.json["id"], request.json["name"], request.json["description"])

    try:
        dtb.add_domain(domain)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    res = make_response({}, 201)
    res.headers['Location'] = url_for(".get_domain", id=domain.id)

    return res


@bp.route("/<int:id>", methods=["PUT"])
def update_domain(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in request.json or "description" not in request.json:
        return jsonify({"error": "Missing data to update"}), 400

    domain = Domain(id, request.json["name"], request.json["description"])

    try:
        dtb.update_domain(domain)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except KeyError:  # raised manually when domain not found
        try:
            dtb.add_domain(domain)
        except oracledb.Error as e:
            return jsonify({"error": str(e)}), 500

        res = make_response({}, 201)
        res.headers['Location'] = url_for(".get_domain", id=id)

        return res

    return {}, 204


@bp.route("/<int:id>", methods=["DELETE"])
def delete_domain(id):
    try:
        dtb.delete_domain(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204
