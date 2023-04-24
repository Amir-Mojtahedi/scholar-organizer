from flask import Blueprint, jsonify, request, abort, flash
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.course import Course

bp = Blueprint('course_api', __name__, url_prefix='/api/courses/')

#Course Page 
@bp.route("/", methods=['GET', 'POST'])
def course_api():
    courses = get_db().get_courses()
    #Add course
    if request.method == 'POST':
        address_json = request.json #In json format
        if address_json:
                address = Address.from_json(address_json) #Turning address_json to "python format"
                try:
                    get_db().add_address(address) 
                    flash("Your address was added")
                except Exception:
                    flash('Address already added')
        #Fetchs precise address
        elif request.method == 'GET':
            if request.args:
                name = request.args.get("name")
                address = [address for address in addresses if address.name == name]
                try:
                    return jsonify(address[0].__dict__)
                except:
                    flash("This address doesn't exist")
        #Return * addresses in json format
        json = [address.__dict__ for address in addresses]
        return jsonify(json)
