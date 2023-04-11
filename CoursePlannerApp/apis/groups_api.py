import oracledb
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db

bp = Blueprint("groups_api", __name__, url_prefix="/api/groups/")

dtb = LocalProxy(get_db)


@bp.route("/<int:group_id>/")
@login_required
def get_group(group_id):
    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2

    if not manages:
        return jsonify({"error": "You do not have permissions to do this action"}), 403

    # get group
    try:
        group = dtb.get_group(group_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not group:
        return jsonify({"error": "Group not found"}), 404

    return jsonify(group)


@bp.route("/<int:group_id>/", methods=["POST"])
@login_required
def add_group(group_id):
    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2

    if not manages:
        return jsonify({"error": "You do not have permissions to do this action"}), 403

    # get group
    try:
        group = dtb.get_group(group_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if group:
        return jsonify({"error": "Group already exists"}), 400

    # get data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "No name provided"}), 400

    # add group
    try:
        dtb.add_group(group_id, name)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200


@bp.route("/<int:group_id>/", methods=["PATCH"])
@login_required
def update_group(group_id):
    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2

    if not manages:
        return jsonify({"error": "You do not have permissions to do this action"}), 403

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
        dtb.update_group(group_id, name)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200


@bp.route("/<int:group_id>/", methods=["DELETE"])
@login_required
def delete_group(group_id):
    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2

    if not manages:
        return jsonify({"error": "You do not have permissions to do this action"}), 403

    # get group
    try:
        group = dtb.get_group(group_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not group:
        return jsonify({"error": "Group not found"}), 404

    # delete group
    try:
        dtb.delete_group(group_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200
