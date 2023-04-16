import oracledb
from flask import Blueprint, jsonify, request
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db

bp = Blueprint("users_api", __name__, url_prefix="/api/users/")

dtb = LocalProxy(get_db)


@bp.route("/")
def get_users():
    # get users
    try:
        users = dtb.get_users()
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if len(users) == 0:
        return jsonify({"error": "No users found"}), 404

    for user in users:
        user.__dict__.pop("password")

    users = [user.__dict__ for user in users]

    return jsonify(users), 200


@bp.route("/<int:user_id>/")
def get_user(user_id):
    # get user
    try:
        user = dtb.get_user(user_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.__dict__.pop("password")
    return jsonify(user.__dict__), 200


@bp.route("/<int:user_id>/", methods=["PATCH"])
def move_user_to_group(user_id):
    # get user
    try:
        user = dtb.get_user(user_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not user:
        return jsonify({"error": "User not found"}), 404

    # get data
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    group_id = data.get("group_id")
    if not group_id:
        return jsonify({"error": "No group_id provided"}), 400

    # update user
    try:
        user.group_id = group_id
        dtb.update_user(user)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200


@bp.route("/<int:user_id>/", methods=["DELETE"])
def remove_user_from_group(user_id):
    # get user
    try:
        user = dtb.get_user(user_id)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    if not user:
        return jsonify({"error": "User not found"}), 404

    # delete user
    try:
        dtb.delete_user(user)
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    return '', 200
