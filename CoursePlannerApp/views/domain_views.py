from flask import Blueprint, redirect, render_template, flash, render_template, request, url_for
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

from CoursePlannerApp.objects.domain import DomainForm, Domain

bp = Blueprint('domains', __name__, url_prefix='/domains')

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
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_domain():
    form = DomainForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            
            newDomain = Domain(form.id.data, form.name.data, form.description.data)
            try:
                dtb.add_domain(newDomain)
                return redirect(url_for('domains.get_domains'))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Domain already exist")
        
            except Exception as e:
                flash("Error: " + str(e))
        else:
            flash('Invalid input')
    return render_template('Add/addDomain.html', form=form)


