from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb
from CoursePlannerApp.objects.element import ElementForm, Element

bp = Blueprint('element', __name__, url_prefix='/elements')

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
@bp.route('/newElement', methods=['GET', 'POST'])
def add_course():
    form = ElementForm()
    if request.method == 'POST' and form.validate_on_submit():
        ##Adding Element to dtb
        try:
            newElement = Element(form.id.data, form.order.data, form.name.data, form.criteria.data, form.competencyId.data) 
            if newElement in dtb.get_elements():
                flash("This element already exist")
            else:
                dtb.add_element(newElement)
        except ValueError as v: 
            flash("Your element is in the wrong format")
        except Exception as e:
            flash("Something wrong happened in the database")
        return render_template('addElement.html', form = form)


