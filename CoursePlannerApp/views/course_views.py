from flask import Blueprint, redirect, render_template, flash, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb
from CoursePlannerApp.objects.course import CourseForm, Course
from CoursePlannerApp.objects.element import Element, ElementFormBridge

bp = Blueprint('courses', __name__, url_prefix='/courses')

dtb = LocalProxy(get_db)

#Get * Courses 
@bp.route("/")
def get_courses():
    if request.method == 'GET':
        try:
            courses = dtb.get_courses()
            domains = dtb.get_domains() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not courses or len(courses) == 0:
            flash('There is no course in database')            
        return render_template('courses.html', courses = courses, domains=domains)
    
@bp.route("/<course_id>/", methods=['GET', 'POST'])
def list_competencies(course_id):
    if request.method == 'GET':
        try:
            course = dtb.get_course(course_id)
            competencies = dtb.get_course_competencies(course_id) 
            elements_covered=dtb.get_elements_covered_by_a_course(course_id)
            domains = dtb.get_domains() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not competencies or len(competencies) == 0:
            flash('There is no competency in the database')            
    return render_template('course.html', competencies = competencies, course = course, domains = domains, elements_covered = elements_covered)

@bp.route('/<course_id>/new/', methods=['GET', 'POST'])
@login_required
def add_element_for_course(course_id):
    form = ElementFormBridge()
    #Fill element drop list
    try:
        elements = dtb.get_elements()
    except Exception:
        flash('There is an issue with the Database')
        
    form.id.choices = sorted([(element.id, str(element.id)+" - "+element.name) for element in elements]) #Getting data for Select field for competencyId  (Circular import error)
    form.id.choices.insert(0, [0, "Choose an Element of Competency"])
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                dtb.add_element_course_bridging(int(form.id.data),course_id,int(form.element_hours.data))
                flash("Element was created successfully.")
                hour_validator(course_id)
                return redirect(url_for('courses.list_competencies',course_id=course_id))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Element already exist")
            
            except Exception as e:
                flash('There is an issue with the Database')

    return render_template('Add/addCourseElementBridge.html', form=form)

#Add course
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()   
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
            
            for course in dtb.get_courses():
                if(newCourse.id == course.id or newCourse.name == course.name):
                    flash("Course already exists!")
                    return redirect(url_for('courses.get_courses'))
            
            try:
                dtb.add_course(newCourse)
                flash("Course has been added")
                hour_validator(form.id.data)    
                return redirect(url_for('courses.list_competencies',course_id=form.id.data))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Course already exist")
        
            except Exception as e:
                flash("Error: " + str(e))
                
    return render_template('Add/addCourse.html', form=form)


#Update course
@bp.route('/<course_id>/update/', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    #Cheack if course exist
    try:
        course = dtb.get_course(course_id)
    except Exception as e:
        flash("Error: "+ str(e))
    
    if course is None:
        flash("Course not found")
        return redirect(url_for('courses.get_courses'))
    
    
    form = CourseForm(obj=course) #Prefill the form
      
    #Creating a new one based on the updated form
    #Fill term drop list
    try:
        terms = dtb.get_terms()
        domains = dtb.get_domains()
    except Exception:
        flash("")
    form.termId.choices = sorted([(term.id, str(term.id)+" - "+term.name) for term in terms]) #Getting data for Select field for termId  (Circular import error)
    form.termId.choices.insert(0, [0, "Choose a term"])

    #Fill domain drop list
    form.domainId.choices = sorted([(domain.id, str(domain.id)+" - "+domain.name) for domain in domains]) #Getting data for Select field for domainId  (Circular import error)
    form.domainId.choices.insert(0, [0, "Choose a domain"])
    
    if request.method == 'POST':
        if form.validate_on_submit():
            
            updatedCourse = Course(form.id.data, form.name.data, form.description.data, 
                               form.termId.data, form.domainId.data, 
                               form.lab_hours.data, form.theory_hours.data, 
                               form.work_hours.data)
            
            # for course in dtb.get_courses():
            #     if( updatedCourse.id == course.id or updatedCourse.name == course.name):
            #         flash("Course already exists!")
                
            try:
                dtb.update_course(updatedCourse, course_id)
                flash("Course has been updated")    
                return redirect(url_for('courses.get_courses'))      
            except Exception as e:
                flash("Error: " + str(e))
                
    return render_template('Update/updateCourse.html', form=form, course=course)

#Delete
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

#Delete an element for specific course
@bp.route('/<course_id>/<int:element_id>/delete/', methods=['GET'])
@login_required
def delete_element_for_course(course_id,element_id):
    try:
        dtb.delete_element_course_bridging(element_id,course_id)
        flash("Element deleted for this course successfully")
        hour_validator(course_id)
    except Exception as e:
        flash("Could not access the record")
        flash("Error: " + str(e))
        return redirect(url_for('courses.list_competencies',course_id=course_id))
    return redirect(url_for('courses.list_competencies',course_id=course_id))

def hour_validator(course_id):
    course=dtb.get_course(course_id)
    total_hours=(course.lab_hours + course.theory_hours) * 15
    current_hours=dtb.get_sum_hours(course_id)
    diff=total_hours-current_hours
    if(diff<0):
        flash(f'You must remove {diff*-1} to match {total_hours} of {course.name}')
    elif(diff>0):
        flash(f'You must add {diff} hours to match {total_hours} hours of {course.id} {course.name}')
