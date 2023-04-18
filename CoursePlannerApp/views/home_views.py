from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
from flask_login import login_required

from CoursePlannerApp.objects.course import CourseForm
from CoursePlannerApp.objects.competency import CompetencyForm
from CoursePlannerApp.objects.domain import DomainForm
from CoursePlannerApp.objects.term import TermForm
from CoursePlannerApp.objects.element import ElementForm

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

@bp.route("/competencies/<course_id>", methods=['GET', 'POST'])
def list_competencies(course_id):
    if request.method == 'GET':
        try:
            competencies = dtb.get_course_competencies(course_id) 
        except Exception as e:
            flash('There is an issue with the Database')
        if not competencies or len(competencies) == 0:
            flash('There is no competency in the database')            
    return render_template('competencies.html', competencies = competencies)

@bp.route("/elements/<competency_id>", methods=['GET', 'POST'])
def list_elements(competency_id):
    if request.method == 'GET':
        try:
            elements = dtb.get_competency_elements(competency_id) 
        except Exception as e:
            flash('There is an issue with the Database')
        if not elements or len(elements) == 0:
            flash('There is no competency in the database')            
    return render_template('elements.html', elements = elements)

@bp.route("/add-course/")
@login_required
def add_course():
    form=CourseForm()
    return render_template('/Add/addCourse.html',form=form)

@bp.route("/add-competency/")
@login_required
def add_competency():
    form=CompetencyForm()
    return render_template('/Add/addCompetency.html',form=form)

@bp.route("/add-domain/")
@login_required
def add_domain():
    form=DomainForm()
    return render_template('/Add/addDomain.html',form=form)

@bp.route("/add-element-of-competency/")
@login_required
def add_element_competency():
    form=ElementForm()
    return render_template('/Add/addElement.html',form=form)

@bp.route("/add-term/")
@login_required
def add_term():
    form=TermForm()
    return render_template('/Add/addTerm.html',form=form)



