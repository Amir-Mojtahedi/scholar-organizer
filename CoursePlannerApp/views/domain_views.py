import oracledb, uuid
from flask import Blueprint, redirect, flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

from CoursePlannerApp.objects.domain import DomainForm, Domain

bp = Blueprint('domains', __name__, url_prefix='/domains')

dtb = LocalProxy(get_db)

#Get * Domains
@bp.route("/")
def get_domains():
    if request.method == 'GET':
        try:
            domains = dtb.get_domains() 
        except Exception as e:
            flash('There is an issue with the Database'+str(e))
            return render_template('domains.html', domains=[])
        
        if not domains or len(domains) == 0:
            flash('There is no domains in the database')
            return render_template('domains.html', domains=[])
        return render_template('domains.html', domains=domains)


@bp.route("/<int:domain_id>/")
def get_domain(domain_id):
    if request.method == 'GET':
        try:
            domain = dtb.get_domain(domain_id) 
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('domain.html', domain=[])
        if not domain:
            flash('There is no domain in the database')
            return render_template('domain.html', domain=[])
        return render_template('domain.html', domain=domain)


#Add Domain
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_domain():
    form = DomainForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            new_domain = Domain(form.name.data, form.description.data)

            try:
                dtb.add_domain(new_domain)
                flash("Domain has been added!")
                return redirect(url_for('domains.get_domains'))

            except Exception as e:
                flash("Error: " + str(e))
        
    return render_template('Add/addDomain.html', form=form)

#Update Domain
@bp.route('/<int:domain_id>/update/', methods=['GET', 'POST'])
@login_required
def update_domain(domain_id):
    
    #Check if domain exist
    try:
        domain = dtb.get_domain(domain_id)
    except Exception as e:
        flash("Error: "+ str(e))
    
    if domain is None:
        flash("Domain not found")
        return redirect(url_for('domains.get_domains'))
    
    form = DomainForm(obj=domain) #Prefill the form
    
    if request.method == 'POST':
        if form.validate_on_submit():

            updated_domain = Domain(form.name.data, form.description.data, id=int(domain_id))

            try:
                dtb.update_domain(updated_domain)
                flash("Domain has been updated")
                return redirect(url_for('domains.get_domains'))
            
            except Exception as e:
                flash("Error: " + str(e))

    return render_template('Update/updateDomain.html', form=form, domain=domain)

#Delete
@bp.route("/<domain_id>/delete/", methods=["GET"])
@login_required
def delete(domain_id):

    try:
        course_impacted = dtb.get_courses_in_domain(domain_id)
    except Exception as e:
        flash("Could not acces the domain")
        flash("Error: " + str(e))
        return redirect(url_for('domains.get_domains'))

    # try to delete domain
    try:
        dtb.delete_domain(domain_id)
        flash("Domain deleted successfully")
    except oracledb.Error as e:
        flash("You can't delete this domain until you delete the following courses or change their domains")
        course_impacted_string = ""
        for course in course_impacted:
            course_impacted_string = f'-- {course.name} --' + course_impacted_string
        flash(course_impacted_string)
    except Exception as e:
        flash("Error: " + str(e))
        return redirect(url_for("domains.get_domains"))

    return redirect(url_for('domains.get_domains'))
