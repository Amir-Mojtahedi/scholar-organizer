from flask import Blueprint, abort, jsonify, request, url_for
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.competency import Competency

bp = Blueprint('competencies_api', __name__, url_prefix='/api/v1/competencies')

from werkzeug.local import LocalProxy

dtb = LocalProxy(get_db)

@bp.route('', methods=['GET', 'POST'])
def competencies_api():
    if request.method == 'POST':
        result = request.json 
        if result:
            competency = Competency.from_json(result)
            dtb.add_competency(competency)
        else:
            abort(400)
    else:
        page_num=1
        if request.args:
            page = request.args.get('page')
            if page:
                page_num = int(page)
        domains, prev_page, next_page = dtb.get_domains(page_num=page_num, page_size=10)
    next_page_url = None
    prev_page_url = None
    if prev_page:
        prev_page_url = url_for('domains_api.domains_api', page=prev_page)
    if next_page:
        next_page_url = url_for('domains_api.domains_api', page=next_page)
    json_domains = {'next_page': next_page_url, 'prev_page': prev_page_url, 'results': [Domain.to_json(domains) for post in posts]}
    return jsonify(json_domains)
