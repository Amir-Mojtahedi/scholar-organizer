from flask_login import login_required
import oracledb
from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.competency import CompetencyForm, Competency

bp = Blueprint("competencies", __name__, url_prefix="/competencies")

dtb = LocalProxy(get_db)

#Get * Competencies
@bp.route("/")
def get_competencies():
    try:
        competencies = dtb.get_competencies()
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return render_template("competencies.html", banner=[])

    if not competencies or len(competencies) == 0:
        flash("There are no competency in database")
    return render_template("competencies.html", competencies=competencies)

@bp.route("/<competency_id>/", methods=['GET', 'POST'])
def list_elements(competency_id):
    if request.method == 'GET':
        try:
            competency = dtb.get_specific_competency(competency_id)
            elements = dtb.get_competency_elements(competency_id) 
        except Exception as e:
            flash('There is an issue with the Database')
        if not elements or len(elements) == 0:
            flash('There is no competency in the database')            
    return render_template('elements.html', elements = elements,competency=competency)

#Add Competency
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_competency():
    form = CompetencyForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            newCompetency = Competency(form.id.data, form.name.data, form.achievement.data, 
                                       form.type.data)
            try:
                dtb.add_competency(newCompetency)
                return redirect(url_for('competencies.get_competencies'))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Competency already exist")
        
            except Exception as e:
                flash("Error: " + str(e))
        else:
            flash('Invalid input')
    return render_template('Add/addCompetency.html', form=form)

#Delete
@bp.route("/<competency_id>/delete/", methods=["GET"])
@login_required
def delete(competency_id):
    
    competency = dtb.get_specific_competency(competency_id)        
    
    #Make sure the user is aware he will also delete associated elements 
    
    # try to delete competency
    try:
        dtb.delete_competency(competency)
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return redirect(url_for('competency.list_elements', 'competency_id=competency.id'))

    flash("Competency deleted successfully")
    return redirect(url_for('competencies.get_competencies'))