import oracledb
from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
from flask_login import login_required

from CoursePlannerApp.objects.course import CourseForm, Course
from CoursePlannerApp.objects.competency import CompetencyForm,Competency
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
    #Fill term drop list
    form.termId.choices = sorted([(term.id, str(term.id)+" - "+term.name) for term in dtb.get_terms()]) #Getting data for Select field for termId  (Circular import error)
    form.termId.choices.insert(0, [0, "Choose a term"])

    #Fill domain drop list
    form.domainId.choices = sorted([(domain.id, str(domain.id)+" - "+domain.name) for domain in dtb.get_domains()]) #Getting data for Select field for domainId  (Circular import error)
    form.domainId.choices.insert(0, [0, "Choose a domain"])
    
    if request.method == 'POST':
        if form.validate_on_submit():
            
            newCourse = Course(form.id.data, form.name.data, form.description.data, 
                               form.termId.data, form.domainId.data, 
                               form.lab_hours.data, form.theory_hours.data, 
                               form.work_hours.data)
            try:
                dtb.add_course(newCourse)
                flash("Course has been added")    
                return redirect(url_for('courses.get_courses'))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Course already exist")
        
            except Exception as e:
                flash("Error: " + str(e))
                
    return render_template('Add/addCourse.html', form=form)

@bp.route("/add-competency/")
@login_required
def add_competency():
    form=CompetencyForm()
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


