import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.apis.competency_api import competency_api
from CoursePlannerApp.dbmanager import get_db
bp = Blueprint('addEntities', __name__, url_prefix='/add')

dtb = LocalProxy(get_db)

#Add Page
@bp.route("/")
def display():
    return render_template('addEntities.html')

#Add Competency
@bp.route('/competencies', methods=["POST"])
def add_competencies():
    form = CompetencyForm()
    if request.method == 'POST' and form.validate_on_submit():
        ##Adding competency to dtb
        try:
            newCompetency = competency_api(form.name.data, form.street.data, form.city.data, form.province.data)
            if newAddress in dtb.get_addresses():
                flash("This address and person already exist")
            else:
                dtb.add_address(newAddress)
        except ValueError as v: 
            flash("Your address is in the wrong format")
        except Exception as e:
            flash("Something wrong happened in the database")
        return render_template('addresses.html', banner = dtb.get_addresses(), form = form)

        try:
            competencies = dtb.get_competencies()
        except oracledb.Error as e:
            flash("Error: " + str(e))
            return render_template('display.html')

        if not competencies or len(competencies) == 0:
            flash("There are no competency in database")
            return render_template('display.html')

        return render_template("competencies.html", banner=competencies)
    return render_template('display.html')

# #Display Courses
# @bp.route('/courses', methods=['GET', 'POST'])
# def display_courses():
#     if request.method == 'GET':
#         try:
#             courses = dtb.get_courses() 
#         except Exception as e:
#             flash('There is an issue with the Database')
#             return render_template('display.html')
        
#         if not courses or len(courses) == 0:
#             flash('There is no course in database')            
#             return render_template('display.html')
        
#         return render_template('courses.html', banner = dtb.get_courses())
#     return render_template('display.html')


# #Display Domains
# @bp.route('/domains', methods=['GET', 'POST'])
# def display_domains():
#     if request.method == 'GET':
#         try:
#             domains = dtb.get_domains() 
#         except Exception as e:
#             flash('There is an issue with the Database')
#             return render_template('display.html')

#         if not domains or len(domains) == 0:
#             flash('There is no domain in database')            
#             return render_template('display.html')

#         return render_template('domains.html', banner = dtb.get_domains())
#     return render_template('display.html')

# #Display Elements
# @bp.route('/elements', methods=['GET', 'POST'])
# def display_elements():
#     if request.method == 'GET':
#         try:
#             elements = dtb.get_elements() 
#         except Exception as e:
#             flash('There is an issue with the Database')
#             return render_template('display.html')
        
#         if not elements or len(elements) == 0:
#             flash('There is no element in database')            
#             return render_template('display.html')
        
#         return render_template('elements.html', banner = dtb.get_elements())
#     return render_template('display.html')

# #Display Terms
# @bp.route('/terms', methods=['GET', 'POST'])
# def display_terms():
#     if request.method == 'GET':
#         try:
#             terms = dtb.get_terms() 
#         except Exception as e:
#             flash('There is an issue with the Database')
#             return render_template('display.html')
        
#         if not terms or len(terms) == 0:
#             flash('There is no term in database') 
#             return render_template('display.html')           
    
#         return render_template('terms.html', banner = dtb.get_terms())
#     return render_template('display.html')




