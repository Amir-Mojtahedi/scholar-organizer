from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

bp = Blueprint('domain', __name__, url_prefix='/domains')

dtb = LocalProxy(get_db)

#Get * Domains
@bp.route("/")
def get_domains():
    try:
        domains = dtb.get_domains() 
    except Exception as e:
        flash("Error: " + str(e))
        return render_template("competencies.html", banner=[])
        
    if not domains or len(domains) == 0:
        flash('There is no domain in database')            
        return render_template('display.html')
    
    return render_template('domains.html', banner = dtb.get_domains())



