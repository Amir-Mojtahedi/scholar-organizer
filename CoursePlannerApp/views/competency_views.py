import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.competency import CompetencyForm, Competency

bp = Blueprint("competency", __name__, url_prefix="/competencies")

dtb = LocalProxy(get_db)

#Get * Competencies
@bp.route("/", methods=["GET"])
def get_competencies():
    try:
        competencies = dtb.get_competencies()
    except oracledb.Error as e:
        flash("Error: " + str(e))
        return render_template("competencies.html", banner=[])

    if not competencies or len(competencies) == 0:
        flash("There are no competency in database")
        return render_template('display.html')

    return render_template("competencies.html", banner=dtb.get_competencies())

#Add course
@bp.route('/newCourse', methods=['GET', 'POST'])
def add_course():
    form = CompetencyForm()
    if request.method == 'POST' and form.validate_on_submit():
        ##Adding course to dtb
        try:
            newCompetency = Competency(form.id.data, form.name.data, form.achievement.data, form.type.data) 
            if newCompetency in dtb.get_courses():
                flash("This competency already exist")
            else:
                dtb.add_course(newCompetency)
        except ValueError as v: 
            flash("Your competency is in the wrong format")
        except Exception as e:
            flash("Something wrong happened in the database")
        return render_template('addCompetency.html', form = form)
