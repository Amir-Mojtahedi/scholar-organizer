import oracledb
from flask import Blueprint, jsonify, request, url_for, make_response
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.term import Term

bp = Blueprint("terms_api", __name__, url_prefix="/api/v1/terms")
dtb = LocalProxy(get_db)


@bp.route("")
def get_terms():
    # pagination
    page = int(request.args.get("page") or 1)

    # get terms
    try:
        terms, prev_page, next_page, count = dtb.get_terms_api(page)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    # pagination urls
    next = url_for(".get_terms", page=next_page) if next_page else None
    prev = url_for(".get_terms", page=prev_page) if prev_page else None

    # add self url to terms
    for term in terms:
        term.url = url_for(".get_term", id=term.id)

    # structure json
    json = {"count": count, "next": next, "prev": prev,
            "results": [term.__dict__ for term in terms]}

    # return json
    return jsonify(json), 200


@bp.route("/<int:id>")
def get_term(id):
    try:
        term = dtb.get_term(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not term:
        return jsonify({"error": "Term not found"}), 404

    term.url = url_for(".get_term", id=term.id)

    return jsonify(term.__dict__), 200


@bp.route("", methods=["POST"])
def add_term():
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "id" not in request.json or "name" not in request.json:
        return jsonify({"error": "Missing data to add"}), 400

    term = Term(request.json["id"], request.json["name"])

    try:
        dtb.add_term(term)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    res = make_response({}, 201)
    res.headers['Location'] = url_for(".get_term", id=term.id)

    return res


@bp.route("/<int:id>", methods=["PUT"])
def update_term(id):
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in request.json:
        return jsonify({"error": "Missing data to update"}), 400

    term = Term(id, request.json["name"])

    try:
        dtb.update_term(term)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500
    except KeyError:  # raised manually when term not found
        try:  # try to add term
            dtb.add_term(term)
        except oracledb.Error as e:
            return jsonify({"error": str(e)}), 500

        res = make_response({}, 201)
        res.headers['Location'] = url_for(".get_term", id=term.id)

        return res

    return {}, 204


@bp.route("/<int:id>", methods=["DELETE"])
def delete_term(id):
    try:
        dtb.delete_term(id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return {}, 204
