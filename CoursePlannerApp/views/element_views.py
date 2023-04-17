from flask import Blueprint, render_template, flash, render_template, request, redirect, url_for
from flask_login import login_required
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb
from CoursePlannerApp.objects.element import ElementForm, Element

from CoursePlannerApp.objects.element import ElementForm, Element

bp = Blueprint('elements', __name__, url_prefix='/elements')

dtb = LocalProxy(get_db)

#Get * Elements
@bp.route("/")
def get_elements():
    try:
        elements = dtb.get_elements() 
    except Exception as e:
        flash("Error: " + str(e))
        return render_template("domains.html", banner=[])
    
    if not elements or len(elements) == 0:
        flash('There is no element in database')            
        return render_template('display.html')
    return render_template('elements.html', banner = dtb.get_elements())

#Add Element
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_element():
    form = ElementForm()
    #Fill competency drop list
    form.competencyId.choices = sorted([(competency.id, str(competency.id)+" - "+competency.name) for competency in dtb.get_competencies()]) #Getting data for Select field for competencyId  (Circular import error)
    form.competencyId.choices.append(['newCompetency', 'Create new competency'])
    form.competencyId.choices.insert(0, [0, "Choose Competency"])
    if request.method == 'POST':
        if form.validate_on_submit():

            if form.competencyId.data == 'newCompetency':
                return redirect(url_for('competencies.create_competency')) #If user want new competency
            
            newElement = Element(form.id.data, form.order.data, form.name.data, 
                                    form.criteria.data, form.competencyId.data)
            try:
                dtb.add_element(newElement)
                return redirect(url_for('elements.get_elements'))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Element already exist")
        
            except Exception as e:
                flash("Error: " + str(e))
        else:
            flash('Invalid input')
    return render_template('Add/addElement.html', form=form)

