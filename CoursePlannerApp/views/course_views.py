from flask import Blueprint, render_template, flash, render_template, request
from werkzeug.local import LocalProxy
from ..dbmanager import get_db
import oracledb

bp = Blueprint('course', __name__, url_prefix='/courses')

dtb = LocalProxy(get_db)

#Get * Courses
@bp.route("/", methods=['GET', 'POST'])
def get_courses():
    if request.method == 'GET':
        try:
            courses = dtb.get_courses() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not courses or len(courses) == 0:
            flash('There is no course in database')            
    return render_template('courses.html', banner = dtb.get_courses())



