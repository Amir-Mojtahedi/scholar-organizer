import oracledb
from flask import Blueprint, flash, render_template
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db

bp = Blueprint("competency", __name__, url_prefix="/competencies/")

dtb = LocalProxy(get_db)


@bp.route("/", methods=["GET"])
def get_competencies():
    try:
        competencies = dtb.get_competencies()
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return render_template("competencies.html", banner=[])

    if not competencies or len(competencies) == 0:
        flash("There are no competency in database")
        return render_template("competencies.html", banner=[])

    return render_template("competencies.html", banner=competencies)
