from flask import Blueprint, render_template, flash, g, redirect, abort, escape, render_template, request, url_for
from werkzeug.local import LocalProxy
from .competency import Competency
from .dbmanager import get_db
import oracledb

bp = Blueprint('competency', __name__, url_prefix='/competencies')

dtb = LocalProxy(get_db)

#Get * Competencies
@bp.route("/", methods=['GET', 'POST'])
def get_competencies():
    if request.method == 'GET':
        ##Fetching address from dtb
        try:
            competencies = dtb.get_competencies() 
        except Exception as e:
            flash('There is an issue with the Database')
        if not competencies or len(competencies) == 0:
            flash('There is no competency in database')            
    return render_template('competencies.html', banner = dtb.get_competencies())



