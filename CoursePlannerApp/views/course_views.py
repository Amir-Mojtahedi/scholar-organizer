from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

from CoursePlannerApp.objects.course import Course, CourseForm

bp = Blueprint('course', __name__, url_prefix='/courses')

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

#Add course
@bp.route('/new/', methods=['GET', 'POST'])
def add_course():
    form = CourseForm()
    if request.method == 'POST' and form.validate_on_submit():
        ##Adding course to dtb
        try:
            newCourse = Course(form.id.data, form.name.data, form.description.data, form.termId.data, form.domainId.data, form.lab_hours.data, form.theory_hours.data, form.work_hours.data) 
            if newCourse in dtb.get_courses():
                flash("This course already exist")
            else:
                dtb.add_course(newCourse)
        except ValueError as v: 
            flash("Your course is in the wrong format")
        except Exception as e:
            flash("Error: " + str(e))
    
    return render_template('/Add/addCourse.html', form = form)


