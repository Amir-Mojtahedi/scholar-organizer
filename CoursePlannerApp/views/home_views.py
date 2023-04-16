from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

dtb = LocalProxy(get_db)

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        try:
            courses = dtb.get_courses() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not courses or len(courses) == 0:
            flash('There is no course in database')            
    return render_template('home.html', courses = courses)

@bp.route("/competencies/<int:course_id>", methods=['GET', 'POST'])
def list_competencies(course_id):
    if request.method == 'GET':
        try:
            elements_of_competency=dtb.get_elements()
            courses = dtb.get_courses()
            competencies = dtb.get_competencies() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not competencies or len(competencies) == 0:
            flash('There is no competency in the database')            
    return render_template('home.html', competencies = competencies)



