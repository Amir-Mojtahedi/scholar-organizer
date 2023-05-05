import oracledb
from flask import Blueprint, redirect, flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.domain import DomainForm, Domain

bp = Blueprint('domains', __name__, url_prefix='/domains')

dtb = LocalProxy(get_db)


# Get * Domains
@bp.route("/")
def get_domains():
    if request.method == 'GET':
        try:
            domains = dtb.get_domains()
        except Exception as e:
            flash('There is an issue with the Database')
        if not domains or len(domains) == 0:
            flash('There is no course in database')
        return render_template('domains.html', domains=domains)


@bp.route("/<int:domain_id>/")
def get_domain(domain_id):
    if request.method == 'GET':
        try:
            domain = dtb.get_domain(domain_id)
        except Exception as e:
            flash('There is an issue with the Database')
        if not domain:
            flash('There is no course in database')
        return render_template('domain.html', domain=domain)


# Add Domain
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_domain():
    form = DomainForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            newDomain = Domain(form.id.data, form.name.data, form.description.data)

            for domain in dtb.get_domains():
                if newDomain.id == domain.id or newDomain.name == domain.name:
                    flash("Domain already exists!")

            try:
                dtb.add_domain(newDomain)
                return redirect(url_for('domains.get_domains'))

            except oracledb.IntegrityError as e:
                error_obj, = e.args  # To acces code error
                if error_obj.code == 1:  # 1 is related to primary key issue (when the primary key already exist)
                    flash("Domain already exist")

            except Exception as e:
                flash("Error: " + str(e))
        else:
            flash('Invalid input')
    return render_template('Add/addDomain.html', form=form)


# Update Domain
@bp.route('/<int:domain_id>/update/', methods=['GET', 'POST'])
@login_required
def update_domain(domain_id):
    # Check if domain exist
    try:
        domain = dtb.get_domain(domain_id)
    except Exception as e:
        flash("Error: " + str(e))

    if domain is None:
        flash("Domain not found")
        return redirect(url_for('domains.get_domains'))

    form = DomainForm(obj=domain)  # Prefill the form

    if request.method == 'POST':
        if form.validate_on_submit():

            updatedDomain = Domain(form.id.data, form.name.data, form.description.data)

            for domain in dtb.get_domains():
                if updatedDomain.id == domain.id or updatedDomain.name == domain.name:
                    flash("Domain already exists!")

            try:
                dtb.update_domain(updatedDomain)
                flash("Domain has been updated")
                return redirect(url_for('domains.get_domains'))
            except Exception as e:
                flash("Error: " + str(e))

    return render_template('Update/updateDomain.html', form=form, domain=domain)


# Delete
@bp.route("/<domain_id>/delete/", methods=["GET"])
@login_required
def delete(domain_id):
    try:
        courseImpacted = dtb.get_courses_in_domain(domain_id)
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
        courseImpactedString = ""
        for course in courseImpacted:
            courseImpactedString = f'-- {course.name} --' + courseImpactedString
        flash(courseImpactedString)
    except Exception as e:
        flash("Error: " + str(e))
        return redirect(url_for("domains.get_domains"))

    return redirect(url_for('domains.get_domains'))
