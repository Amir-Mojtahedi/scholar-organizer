from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

bp = Blueprint('element', __name__, url_prefix='/elements')

dtb = LocalProxy(get_db)

#Get * Elements
@bp.route("/", methods=['GET', 'POST'])
def get_elements():
    if request.method == 'GET':
        try:
            elements = dtb.get_elements() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not elements or len(elements) == 0:
            flash('There is no element in database')            
    return render_template('elements.html', banner = dtb.get_elements())



