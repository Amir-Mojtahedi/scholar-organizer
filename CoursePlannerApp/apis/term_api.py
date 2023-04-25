# import math
# from flask import Blueprint, abort, jsonify, make_response, request, flash, url_for, redirect
# from ..dbmanager import get_db
# from ..DBobjects.term import Term
# from ..APIObject.collection import APIMulipleCollection, APISingleCollection
# import datetime

# bp = Blueprint('api_term', __name__, url_prefix='/api/terms')

# @bp.route('/', methods=['GET','POST'])
# def terms_api(): 
#     # Try except block that gets the page courses and the db
#     try:
#         db = get_db()
#         count = db.get_terms_count()
#         page = int(request.args.get('page', 1))
#         offset = (page - 1) * 3
#         terms = db.get_terms_three(offset)
#     except Exception as e:
#         abort(404)
#     num_pages = math.ceil(count / 3)
#     prev_link = None
#     next_link = None

#     if page > 1:
#         prev_link = url_for('api_term.terms_api',page=page-1)
#     if page < num_pages:
#         next_link = url_for('api_term.terms_api',page=page+1)
#     # POST METHOD
#     if request.method == 'POST':
#         term_json = request.json
#         if term_json:
#             term = Term.from_json(term_json)
#             try:
#                 db.add_term(term)
#                 resp = make_response({},201)
#                 resp.headers['Location'] = url_for('api_term.get_term_api', id = term.id)
#                 return resp
#             except Exception as e:
#                 abort(409)
#         else:
#             abort(400)
#     # GET METHOD THAT RETURNS A SINGULAR BY FILTERING
#     elif request.method == 'GET':
#         if request.args.get("id"):
#             id = request.args.get("id")
#             try: 
#                 id = int(id)
#                 term = db.get_term(id)
#                 collection = APISingleCollection(count, prev_link, next_link, num_pages, term.to_json(), request.url, len(terms))
#                 return jsonify(collection.to_json())
#             except:
#                 return jsonify({})
#         if request.args.get("page"):
#             page_num = int(request.args.get("page"))
#             if page_num > num_pages:
#                 return jsonify({})
#     json_terms = [term.to_json() for term in terms]
#     collection = APIMulipleCollection(count, prev_link, next_link, num_pages, json_terms, request.url, len(terms))
#     return jsonify(collection.to_json())


# @bp.route('/<int:id>', methods=['GET','DELETE','PUT'])
# def get_term_api(id):
#     try:
#         db = get_db()
#     except Exception as e:
#         abort(404)
#     # DELETE METHOD
#     if request.method == 'DELETE':
#         try:
#              id = int(id)
#             db.delete_term(id)
#             resp = make_response({},204)
#             return resp
#         except Exception as e:
#             abort(409)
#     # PUT METHOD THAT UPDATES 
#     # YOU NEED TO PUT THE ID IN THE URL AND IT HAS TO MATCH THE COURSE ID GIVEN
#     elif request.method == 'PUT':
#         term_json = request.json
#         if term_json:
#             term = Term.from_json(term_json)
#             if term.id == id:
#                 try:
#                     db.update_term(term)
#                     resp = make_response({},201)
#                     resp.headers['Location'] = url_for('api_term.get_term_api', id = term.id)
#                     return resp
#                 except Exception as e:
#                     abort(409)
#         else:
#             abort(400)
#     try: 
#         term = db.get_term(id)
#         return jsonify(term.to_json())
#     except:
#         return jsonify({})