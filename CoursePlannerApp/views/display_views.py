from flask import Blueprint, render_template, url_for

bp = Blueprint('display', __name__, url_prefix='/display')

#HOMEPAGE
@bp.route("/")
def display():
    return render_template('display.html')

