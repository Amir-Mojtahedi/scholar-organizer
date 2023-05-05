import oracledb
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_required
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.competency import CompetencyForm, Competency

bp = Blueprint("competencies", __name__, url_prefix="/competencies")

dtb = LocalProxy(get_db)


# Get * Competencies
@bp.route("/")
def get_competencies():
    try:
        competencies = dtb.get_competencies()
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return render_template("competencies.html", competencies=[])

    if not competencies or len(competencies) == 0:
        flash("There are no competency in database")
    return render_template("competencies.html", competencies=competencies)


@bp.route("/<competency_id>/", methods=['GET', 'POST'])
def list_elements(competency_id):
    if request.method == 'GET':
        try:
            competency = dtb.get_competency(competency_id)
            elements = dtb.get_competency_elements(competency_id)
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('competency.html', elements=[], competency=[])
        if not elements or len(elements) == 0:
            flash('There is no competency in the database')
    return render_template('competency.html', elements=elements, competency=competency)


# Add Competency
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_competency():
    form = CompetencyForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            new_competency = Competency(form.id.data, form.name.data, form.achievement.data,
                                       form.type.data)

            try:
                dtb.add_competency(new_competency)
                flash("Competency was added!")
                return redirect(url_for('competencies.get_competencies'))

            except Exception as e:
                flash("Error: " + str(e))
                
    return render_template('Add/addCompetency.html', form=form)


# Update competency
@bp.route('/<competency_id>/update/', methods=['GET', 'POST'])
@login_required
def update_competency(competency_id):
    # Check if competency exist
    try:
        competency = dtb.get_competency(competency_id)
    except Exception as e:
        flash("Error: " + str(e))

    if competency is None:
        flash("Competency not found")
        return redirect(url_for('competencies.get_competencies'))

    form = CompetencyForm(obj=competency)  # Prefill the form

    if request.method == 'POST':
        if form.validate_on_submit():

            updatedCompetency = Competency(form.id.data, form.name.data, form.achievement.data,
                                           form.type.data)

            try:
                dtb.update_competency(updatedCompetency)
                flash("Competency has been updated")
                return redirect(url_for('competencies.get_competencies'))
            except Exception as e:
                flash("Error: " + str(e))

    return render_template('Update/updateCompetency.html', form=form, competency=competency)


# Delete
@bp.route("/<competency_id>/delete/", methods=["GET"])
@login_required
def delete(competency_id):
    
    # try to delete competency
    try:
        dtb.delete_competency(competency_id)
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return redirect(url_for('competency.list_elements', competency_id=competency_id))

    flash("Competency deleted successfully")
    return redirect(url_for('competencies.get_competencies'))
