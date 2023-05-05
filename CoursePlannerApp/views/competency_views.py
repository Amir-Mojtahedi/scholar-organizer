from flask_login import login_required
import oracledb
from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.competency import CompetencyForm, Competency
from CoursePlannerApp.objects.element import Element, ElementForm

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

# List all the elements of a specific competency
@bp.route("/<competency_id>/", methods=['GET', 'POST'])
def list_elements(competency_id):
    if request.method == 'GET':
        try:
            competency = dtb.get_competency(competency_id)
            elements = dtb.get_competency_elements(competency_id) 
        except Exception as e:
            flash('There is an issue with the Database')
        if not elements or len(elements) == 0:
            flash('There is no competency in the database')            
    return render_template('competency.html', elements = elements,competency=competency)

#Create Competency
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_competency():
    form = CompetencyForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            newCompetency = Competency(form.id.data, form.name.data, form.achievement.data, 
                                       form.type.data)

            try:
                competencies = dtb.get_competencies() 
            except Exception:
                flash('There is an issue with the Database')
                
            for competency in competencies:
                if(newCompetency.id == competency.id or newCompetency.name == competency.name):
                    flash("Competency already exists!")
            
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

#Update competency
@bp.route('/<competency_id>/update/', methods=['GET', 'POST'])
@login_required
def update_competency(competency_id):
    oldCompetencyId = competency_id
    #Check if competency exist
    try:
        competency = dtb.get_competency(competency_id)
    except Exception as e:
        flash("Error: "+ str(e))
    
    if competency is None:
        flash("Competency not found")
        return redirect(url_for('competencies.get_competencies'))
    
    form = CompetencyForm(obj=competency) #Prefill the form
    
    if request.method == 'POST':
        if form.validate_on_submit():

            updatedCompetency = Competency(form.id.data, form.name.data, form.achievement.data, 
                                       form.type.data)
            
            for competency in dtb.get_competencies():
                if(updatedCompetency.id == competency.id or updatedCompetency.name == competency.name):
                    flash("Competency already exists!")
                
            try:
                dtb.update_competency(updatedCompetency, oldCompetencyId)
                flash("Competency has been updated")    
                return redirect(url_for('competencies.get_competencies'))
            except Exception as e:
                flash("Error: " + str(e))

    return render_template('Update/updateCompetency.html', form=form, competency=competency)

#Delete competency
@bp.route("/<competency_id>/delete/", methods=["GET"])
@login_required
def delete(competency_id):
    try:
        competency = dtb.get_competency(competency_id)
    except Exception as e:
        flash("Could not acces the competency")
        return redirect(url_for('competency.list_elements', competency_id=competency.id))
    
    # try to delete competency
    try:
        dtb.delete_competency(competency.id)
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return redirect(url_for('competency.list_elements', 'competency_id=competency.id'))

    flash("Competency deleted successfully")
    return redirect(url_for('competencies.get_competencies'))

#Add an Element to the competency
@bp.route('/<competency_id>/new-element/', methods=['GET', 'POST'])
# @login_required
def create_element(competency_id):
    form = ElementForm()
    form.competencyId.choices.append(competency_id)
    # The form will have by default the competency id of the clicked competency.
    form.competencyId.data=competency_id
    if request.method == 'POST':
        if form.validate_on_submit():
            
            newElement = Element(0,form.order.data, form.name.data, 
                                    form.criteria.data, form.competencyId.data)
            try:
                dtb.add_element(newElement)
                flash('Element was created successfully')
                return redirect(url_for('competencies.list_elements',competency_id=competency_id))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Element already exist")
        
            except Exception as e:
                flash("Error: " + str(e))
        else:
            flash('Invalid input')
    return render_template('Add/addElement.html', form=form)


# Update an element of the competency
@bp.route('/<competency_id>/<int:element_id>/update-element/', methods=['GET', 'POST'])
#@login_required
def update_element(competency_id,element_id):
    
    #Check if element exist
    try:
        element = dtb.get_element(element_id)
    except Exception as e:
        flash("Error: "+ str(e))
    
    if element is None:
        flash("Element not found")
        return redirect(url_for('competencies.list_elements',competency_id=competency_id))
    
    form = ElementForm(obj=element)
    #Prefill the form
    form.competencyId.choices.append(competency_id)
    # The form will have by default the competency id of the clicked competency.
    form.competencyId.data=competency_id

    if request.method == 'POST':
        if form.validate_on_submit():

            updatedElement = Element(element_id, form.order.data, form.name.data, 
                                    form.criteria.data, form.competencyId.data)
            try:
                dtb.update_element(updatedElement)
                flash("Element has been updated")    
                return redirect(url_for('competencies.list_elements',competency_id=competency_id))
            except Exception as e:
                flash("Error: " + str(e))

    return render_template('Update/updateElement.html', form=form, element=element)

#Delete an element of competency
@bp.route("/<competency_id>/<int:element_id>/delete/", methods=["GET"])
# @login_required
def delete_element(competency_id,element_id):

    try:
        element = dtb.get_element(element_id)
        # try to delete element
        dtb.delete_element(element.id)
        flash("Element deleted successfully")
    except Exception as e:
        flash("Error: " + str(e))
        return redirect(url_for('competencies.list_elements', competency_id=element.competencyId))
    
    return redirect(url_for('competencies.list_elements', competency_id=competency_id))
