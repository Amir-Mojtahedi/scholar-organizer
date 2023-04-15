import oracledb
from flask import Blueprint, jsonify, request
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.group import Group

bp = Blueprint("groups_api", __name__, url_prefix="/api/groups/")

dtb = LocalProxy(get_db)


@bp.route("/")
def get_groups():
    # get groups
    try:
        groups = dtb.get_groups()
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if len(groups) == 0:
        return jsonify({"error": "No groups found"}), 404

    # try jsonifying
    try:
        groups = [group.to_dict() for group in groups]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(groups), 200


@bp.route("/<int:group_id>/")
def get_group(group_id):
    # get group
    try:
        group = dtb.get_group(group_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not group:
        return jsonify({"error": "Group not found"}), 404

    return jsonify(group), 200


@bp.route("/", methods=["POST"])
def add_group():
    # get data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "No name provided"}), 400

    try:
        group = Group(name=name)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # add group
    try:
        dtb.add_group(group)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200


@bp.route("/<int:group_id>/", methods=["PATCH"])
def update_group(group_id):
    # get group
    try:
        group = dtb.get_group(group_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not group:
        return jsonify({"error": "Group not found"}), 404

    # get data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "No name provided"}), 400

    # update group
    try:
        group.name = name
        dtb.update_group(group)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200


@bp.route("/<int:group_id>/", methods=["DELETE"])
def delete_group(group_id):
    # get group
    try:
        group = dtb.get_group(group_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not group:
        return jsonify({"error": "Group not found"}), 404

    # delete group
    try:
        dtb.delete_group(group)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200
