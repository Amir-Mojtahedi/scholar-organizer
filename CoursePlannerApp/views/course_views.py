from flask import Blueprint, redirect, render_template, flash, render_template, request, url_for
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb
from CoursePlannerApp.objects.course import CourseForm, Course

bp = Blueprint('courses', __name__, url_prefix='/courses')

dtb = LocalProxy(get_db)

#Get * Courses
@bp.route("/")
def get_courses():
    try:
        courses = dtb.get_courses() 
    except Exception as e:
        flash("Error: " + str(e))
        return render_template("courses.html", banner=[])

    if not courses or len(courses) == 0:
        flash('There is no course in database')       
        return render_template('display.html')
    return render_template('courses.html', banner = dtb.get_courses())

@bp.route('/new/', methods=['GET', 'POST'])
def create_course():
    form = CourseForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            newCourse = Course(form.id.data, form.name.data, form.description.data, 
                               form.termId.data, form.domainId.data, 
                               form.lab_hours.data, form.theory_hours.data, 
                               form.work_hours.data)
            try:
                dtb.add_course(newCourse)
                return redirect(url_for('courses.get_courses'))
            
            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error 
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist) 
                    flash("Course already exist")
        
            except Exception as e:
                flash("Error: " + str(e))
        else:
            flash('Invalid input')
    return render_template('Add/addCourse.html', form=form)

