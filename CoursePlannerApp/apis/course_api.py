from flask import Blueprint, jsonify, make_response, request, abort, flash, url_for
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.course import Course

bp = Blueprint('course_api', __name__, url_prefix='/api/courses/')

#Course Page 
@bp.route("/", methods=['GET', 'POST'])
def course_api():
    #Get needed data
    try:
        courses = get_db().get_courses()
    except Exception:
        abort(404)
    #Add course
    if request.method == 'POST':
        course_json = request.json #In json format
        if course_json:
                course = Course.from_json(course_json) #Turning _json to "python format"
                try:
                    get_db().add_course(course) 
                    resp = make_response({}, 201)
                    resp.headers['Location'] = url_for('')
                    flash("Your address was added")
                except Exception:
                    abort(400) 
        else:
            abort(400)
    #Fetchs precise course
    elif request.method == 'GET':
        if request.args:
            courseId = request.args.get("id")
            try:
                course = [course for course in courses if course.id == courseId]
                return jsonify(course[0].__dict__)
            except Exception:
                flash("This course doesn't exist")

    
    #Return * courses in json format
    json = [course.__dict__ for course in courses]
    return jsonify(json)

@bp.route('/<courseId>', methods=['GET','DELETE','PUT'])
def get_course_api(courseId):
    try:
        db = get_db()
    except Exception as e:
        abort(404)
    # DELETE METHOD
    if request.method == 'DELETE':
        try:
            db.delete_course(courseId)
            resp = make_response({},204)
            return resp
        except Exception as e:
            abort(409)
    # PUT METHOD THAT UPDATES 
    # YOU NEED TO PUT THE ID IN THE URL AND IT HAS TO MATCH THE COURSE ID GIVEN
    elif request.method == 'PUT':
        course_json = request.json
        if course_json:
            course = Course.from_json(course_json)
            if course.id == id:
                try:
                    db.update_course(course)
                    resp = make_response({},201)
                    resp.headers['Location'] = url_for('course_api.get_course_api', id = course.id)
                    return resp
                except Exception as e:
                    abort(409)
        else:
            abort(400)
    try: 
        nCourse = db.get_specific_course(course.id)
        return jsonify(nCourse.to_json())
    except:
        return jsonify({})