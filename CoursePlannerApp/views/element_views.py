from flask import Blueprint, render_template, flash, render_template, request, redirect, url_for
from flask_login import login_required
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb
from CoursePlannerApp.objects.element import ElementForm, Element

bp = Blueprint('elements', __name__, url_prefix='/elements')

dtb = LocalProxy(get_db)


# Get * Elements
@bp.route("/")
def get_elements():
    try:
        elements = dtb.get_competencies()
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return render_template("elements.html", elements=[])

    if not elements or len(elements) == 0:
        flash("There are no competency in database")
    return render_template("elements.html", elements=elements)

#Add an Element to the competency
@bp.route('/<competency_id>/new-element/', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
