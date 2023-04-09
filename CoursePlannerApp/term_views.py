from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from .dbmanager import get_db
import oracledb

bp = Blueprint('term', __name__, url_prefix='/terms')

dtb = LocalProxy(get_db)

#Get * Terms
@bp.route("/", methods=['GET', 'POST'])
def get_terms():
    if request.method == 'GET':
        try:
            terms = dtb.get_terms() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not terms or len(terms) == 0:
            flash('There is no term in database')            
    return render_template('terms.html', banner = dtb.get_terms())



