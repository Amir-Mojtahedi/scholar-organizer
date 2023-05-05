from flask import Blueprint, render_template, flash, render_template, request, redirect, url_for
from flask_login import login_required
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb

from CoursePlannerApp.objects.term import TermForm, Term

bp = Blueprint('terms', __name__, url_prefix='/terms')

dtb = LocalProxy(get_db)

#Get * Terms
@bp.route("/")
def get_terms():
    try:
        terms = dtb.get_terms()
    except Exception as e:
        flash("Error: " + str(e))
        return render_template("terms.html", terms=[])

    if not terms or len(terms) == 0:
        flash('There is no term in database')
        return render_template('display.html')
    return render_template('terms.html', terms = dtb.get_terms())

#Add term
@bp.route('/new/', methods=['GET', 'POST'])
@login_required
def create_term():
    form = TermForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            newTerm = Term(form.id.data, form.name.data)
            try:
                dtb.add_term(newTerm)
                return redirect(url_for('terms.get_terms'))

            except oracledb.IntegrityError as e:
                error_obj, = e.args #To acces code error
                if error_obj.code == 1: # 1 is related to primary key issue (when the primary key already exist)
                    flash("Course already exist")

            except Exception as e:
                flash("Error: " + str(e))
        else:
            flash('Invalid input')
    return render_template('Add/addTerm.html', form=form)

#Update term
@bp.route('/<term_id>/update/', methods=['GET', 'POST'])
@login_required
def update_term(term_id):

    #Check if term exist
    try:
        term = dtb.get_term(term_id)
    except Exception as e:
        flash("Error: "+ str(e))

    if term is None:
        flash("Term not found")
        return redirect(url_for('terms.get_terms'))

    form = TermForm(obj=term) #Prefill the form

    if request.method == 'POST':
        if form.validate_on_submit():

            updatedTerm = Term(term_id, form.name.data)
            try:
                dtb.update_term(updatedTerm)
                flash("Term has been updated")
                return redirect(url_for('terms.get_terms'))
            except Exception as e:
                flash("Error: " + str(e))

    return render_template('Update/updateTerm.html', form=form, term=term)

#Delete
@bp.route("/<term_id>/delete/", methods=["GET"])
@login_required
def delete(term_id):

    try:
        courseImpacted = dtb.get_courses_in_term(term_id)
    except Exception as e:
        flash("Could not acces the term")


    # try to delete term
    try:
        dtb.delete_term(term_id)
        flash("Term deleted successfully")
    except oracledb.Error as e:
        flash("You can't delete this term until you delete the following courses or change their domains")
        courseImpactedString = ""
        for course in courseImpacted:
            courseImpactedString = f'-- {course.name} --'+ courseImpactedString
        flash(courseImpactedString)
    except Exception as e:
        flash("Error: " + str(e))
        return redirect(url_for("terms.get_terms"))

    return redirect(url_for("terms.get_terms"))