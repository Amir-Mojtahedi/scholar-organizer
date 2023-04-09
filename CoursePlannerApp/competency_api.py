import oracledb
from flask import Blueprint, jsonify
from werkzeug.local import LocalProxy

from .dbmanager import get_db

bp = Blueprint("competency_api", __name__, url_prefix="/api/competencies/")

dtb = LocalProxy(get_db)


@bp.route("/", methods=["GET", "POST"])
def competencies_api():
    try:
        competencies = dtb.get_competencies()
    except oracledb.Error as e:
        return jsonify({"error": str(e)}), 500

    # Return * competencies in json format
    json = [competency.__dict__ for competency in competencies]
    return jsonify(json)
