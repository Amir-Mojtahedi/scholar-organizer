import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
from flask_login import login_required

from CoursePlannerApp.objects.course import CourseForm
from CoursePlannerApp.objects.competency import CompetencyForm
from CoursePlannerApp.objects.domain import DomainForm
from CoursePlannerApp.objects.term import TermForm
from CoursePlannerApp.objects.element import ElementForm

bp = Blueprint('add', __name__, url_prefix='/add')

dtb = LocalProxy(get_db)

@bp.route("/")
def index():
    return render_template('/Add/add.html')

@bp.route("/add-course/")
@login_required
def add_course():
    form=CourseForm()
    options= dtb.get_terms()
    form.termId.choices=options
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


