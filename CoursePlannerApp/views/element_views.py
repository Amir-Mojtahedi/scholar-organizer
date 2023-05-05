from flask import Blueprint, render_template, flash, render_template, request, redirect, url_for
from flask_login import login_required
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
import oracledb
from CoursePlannerApp.objects.element import ElementForm, Element

from CoursePlannerApp.objects.element import ElementForm, Element

bp = Blueprint('elements', __name__, url_prefix='/elements')


