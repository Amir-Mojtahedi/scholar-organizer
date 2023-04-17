from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

from CoursePlannerApp.objects.domain import Domain, DomainForm

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

#Add Domain
@bp.route('/newDomain', methods=['GET', 'POST'])
def add_course():
    form = DomainForm()
    if request.method == 'POST' and form.validate_on_submit():
        ##Adding Domain to dtb
        try:
            newDomain = Domain(form.id.data, form.name.data, form.description.data) 
            if newDomain in dtb.get_domains():
                flash("This domain already exist")
            else:
                dtb.add_domain(newDomain)
        except ValueError as v: 
            flash("Your domain is in the wrong format")
        except Exception as e:
            flash("Something wrong happened in the database")
        return render_template('addDomain.html', form = form)



