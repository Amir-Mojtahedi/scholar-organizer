import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
bp = Blueprint('display', __name__, url_prefix='/display')

dtb = LocalProxy(get_db)

#Display Page
@bp.route("/")
def display():
    return render_template('display.html')

#Display Competencies
@bp.route('/competencies', methods=["GET"])
def display_competencies():
    if request.method == 'GET':
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

#Display Courses
@bp.route('/courses', methods=['GET', 'POST'])
def display_courses():
    if request.method == 'GET':
        try:
            courses = dtb.get_courses() 
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('display.html')
        
        if not courses or len(courses) == 0:
            flash('There is no course in database')            
            return render_template('display.html')
        
        return render_template('courses.html', banner = dtb.get_courses())
    return render_template('display.html')


#Display Domains
@bp.route('/domains', methods=['GET', 'POST'])
def display_domains():
    if request.method == 'GET':
        try:
            domains = dtb.get_domains() 
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('display.html')

        if not domains or len(domains) == 0:
            flash('There is no domain in database')            
            return render_template('display.html')

        return render_template('domains.html', banner = dtb.get_domains())
    return render_template('display.html')

#Display Elements
@bp.route('/elements', methods=['GET', 'POST'])
def display_elements():
    if request.method == 'GET':
        try:
            elements = dtb.get_elements() 
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('display.html')
        
        if not elements or len(elements) == 0:
            flash('There is no element in database')            
            return render_template('display.html')
        
        return render_template('elements.html', banner = dtb.get_elements())
    return render_template('display.html')

#Display Terms
@bp.route('/terms', methods=['GET', 'POST'])
def display_terms():
    if request.method == 'GET':
        try:
            terms = dtb.get_terms() 
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('display.html')
        
        if not terms or len(terms) == 0:
            flash('There is no term in database') 
            return render_template('display.html')           
    
        return render_template('terms.html', banner = dtb.get_terms())
    return render_template('display.html')




