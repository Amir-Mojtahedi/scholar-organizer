from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

bp = Blueprint('domain', __name__, url_prefix='/domains')

dtb = LocalProxy(get_db)

#Get * Domains
@bp.route("/", methods=['GET', 'POST'])
def get_domains():
    if request.method == 'GET':
        try:
            domains = dtb.get_domains() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not domains or len(domains) == 0:
            flash('There is no domain in database')            
    return render_template('domains.html', banner = dtb.get_domains())



