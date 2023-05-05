import oracledb
from flask import Blueprint, redirect, flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.course import CourseForm, Course
from CoursePlannerApp.objects.element import ElementFormBridge

bp = Blueprint('courses', __name__, url_prefix='/courses')

dtb = LocalProxy(get_db)


# Get * Courses
@bp.route("/")
def get_courses():
    if request.method == 'GET':
        try:
            courses = dtb.get_courses()
            domains = dtb.get_domains()
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('courses.html', courses=[], domains=[])
        
        if not courses or len(courses) == 0:
            flash('There is no course in database')
        
        return render_template('courses.html', courses=courses, domains=domains)


@bp.route("/<course_id>/", methods=['GET', 'POST'])
def list_competencies(course_id):
    if request.method == 'GET':
        try:
            course = dtb.get_course(course_id)
            competencies = dtb.get_course_competencies(course_id)
            elements_covered = dtb.get_elements_covered_by_a_course(course_id)
            domains = dtb.get_domains()
        except Exception as e:
            flash('There is an issue with the Database')
            return render_template('courses.html', courses=[], domains=[], competencies=[], elements_covered=[])
        
        if not competencies or len(competencies) == 0:
            flash('There is no competency in the database')
    
    return render_template('course.html', competencies=competencies, course=course, domains=domains,
                           elements_covered=elements_covered)


@bp.route('/<course_id>/new/', methods=['GET', 'POST'])
@login_required
def add_element_for_course(course_id):
    form = ElementFormBridge()
    # Fill element drop list
    try:
        elements = dtb.get_elements()
    except Exception:
        flash('There is an issue with the Database')
        
    form.id.choices = sorted([(element.id, str(element.id) + " - " + element.name) for element in
                             elements])  # Getting data for Select field for competencyId 
    form.id.choices.insert(0, [0, "Choose an Element of Competency"])
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                dtb.add_element_course_bridging(int(form.id.data), course_id, int(form.element_hours.data))
                flash("Element was created successfully.")
                hour_validator(course_id)
                return redirect(url_for('courses.list_competencies', course_id=course_id))

            except oracledb.IntegrityError as e:
                error_obj, = e.args  # To acces code error
                if error_obj.code == 1:  # 1 is related to primary key issue (when the primary key already exist)
                    flash("Element already exist")

            except Exception as e:
                flash('There is an issue with the Database')
                return render_template('courses.html', courses=[], domains=[])
            
    return render_template('Add/addCourseElementBridge.html', form=form)


# Add course
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    try:
        terms = dtb.get_terms()
        domains = dtb.get_domains()
    except Exception:
        flash("There is an issue with the database")
        
    # Fill term drop list
    form.term_id.choices = sorted([(term.id, str(term.id) + " - " + term.name) for term in terms])
    form.term_id.choices.insert(0, [0, "Choose a term"])
    form.term_id.choices.append(['newTerm', "Create new term"])
    
    # Fill domain drop list
    form.domain_id.choices = sorted([(domain.id, str(domain.id) + " - " + domain.name) for domain in domains]) 
    form.domain_id.choices.insert(0, [0, "Choose a domain"])
    form.domain_id.choices.append(['newDomain', "Create new domain"])

    if request.method == 'POST':
        if form.validate_on_submit():
            
            if form.term_id.data == 'newTerm':
                return redirect(url_for('terms.create_term')) #If user want new term
            
            if form.domain_id.data == 'newDomain':
                return redirect(url_for('domains.create_domain')) #If user want new domain

            new_course = Course(form.id.data, form.name.data, form.description.data,
                               form.term_id.data, form.domain_id.data,
                               form.lab_hours.data, form.theory_hours.data,
                               form.work_hours.data)

            try:
                dtb.update_course(new_course)
                flash("Course has been updated")    
                return redirect(url_for('courses.get_courses'))      
            except Exception as e:
                flash("Error: " + str(e))


    return render_template('Add/addCourse.html', form=form)


# Update course
@bp.route('/<course_id>/update/', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    # Cheack if course exist
    try:
        course = dtb.get_course(course_id)
    except Exception as e:
        flash("Error: " + str(e))

    if course is None:
        flash("Course not found")
        return redirect(url_for('courses.get_courses'))

    form = CourseForm(obj=course)  # Prefill the form

    # Creating a new one based on the updated form
    # Fill term drop list
    try:
        terms = dtb.get_terms()
        domains = dtb.get_domains()
    except Exception:
        flash("Error: "+ str(e))
        
    form.term_id.choices = sorted([(term.id, str(term.id) + " - " + term.name) for term in terms])
    form.term_id.choices.insert(0, [0, "Choose a term"])
    form.term_id.choices.append(['newTerm', "Create new term"])

    # Fill domain drop list
    form.domain_id.choices = sorted([(domain.id, str(domain.id) + " - " + domain.name) for domain in domains])  
    form.domain_id.choices.insert(0, [0, "Choose a domain"])
    form.domain_id.choices.append(['newDomain', "Create new domain"])

    if request.method == 'POST':
        if form.validate_on_submit():
            
            if form.term_id.data == 'newTerm':
                return redirect(url_for('terms.create_term')) #If user want new term
            
            if form.domain_id.data == 'newDomain':
                return redirect(url_for('domains.create_domain')) #If user want new domain

            updated_course = Course(form.id.data, form.name.data, form.description.data,
                                   form.term_id.data, form.domain_id.data,
                                   form.lab_hours.data, form.theory_hours.data,
                                   form.work_hours.data)

            try:
                dtb.update_course(updated_course)
                flash("Course has been updated")
                return redirect(url_for('courses.get_courses'))
            except Exception as e:
                flash("Error: " + str(e))

    return render_template('Update/updateCourse.html', form=form, course=course)


# Delete
@bp.route("/<course_id>/delete/", methods=["GET"])
@login_required
def delete(course_id):
    # try to delete course
    try:
        dtb.delete_course(course_id)
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return redirect(url_for(".get_courses"))

    flash("Course deleted successfully")
    return redirect(url_for('courses.get_courses'))


# Delete an element for specific course
@bp.route('/<course_id>/<int:element_id>/delete/', methods=['GET'])
@login_required
def delete_element_for_course(course_id, element_id):
    try:
        dtb.delete_element_course_bridging(element_id, course_id)
        flash("Element deleted for this course successfully")
        hour_validator(course_id)
    except Exception as e:
        flash("Could not access the record")
        flash("Error: " + str(e))
        return redirect(url_for('courses.list_competencies', course_id=course_id))
    return redirect(url_for('courses.list_competencies', course_id=course_id))


def hour_validator(course_id):
    course = dtb.get_course(course_id)
    total_hours = (course.lab_hours + course.theory_hours) * 15
    current_hours = dtb.get_sum_hours(course_id)
    diff = total_hours - current_hours
    if (diff < 0):
        flash(f'You must remove {diff * -1} to match {total_hours} of {course.name}')
    elif (diff > 0):
        flash(f'You must add {diff} hours to match {total_hours} hours of {course.id} {course.name}')
