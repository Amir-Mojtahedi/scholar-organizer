import flask_unittest
from CoursePlannerApp import create_app
from CoursePlannerApp.objects.domain import Domain
from CoursePlannerApp.objects.term import Term

class TestForAPI(flask_unittest.ClientTestCase):
    app = create_app()

    # --------------- START DOMAIN CRUD TEST ---------------
    def test_get_domains(self, client):
        resp = client.get('/api/v1/domains')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        domain = Domain(1,"Programming, Data Structures, and Algorithms","The courses in the Programming, Data Structures and Algorithms domain teach the knowledge and skills required to design and program solutions to typical information technology problems. The students are taught object-oriented programming in the context of standalone, event-driven and web-based programs.")
        json_domain = Domain(json['results'][0]['id'],json['results'][0]['name'],json['results'][0]['description'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertEqual(json_domain.id,domain.id)
        self.assertEqual(json_domain.name,domain.name)
        self.assertEqual(json_domain.description,domain.description)
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_domain(self,client):
        resp = client.get('/api/v1/domains/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        domain = Domain(1,"Programming, Data Structures, and Algorithms","The courses in the Programming, Data Structures and Algorithms domain teach the knowledge and skills required to design and program solutions to typical information technology problems. The students are taught object-oriented programming in the context of standalone, event-driven and web-based programs.")
        json_domain = Domain(json['id'],json['name'],json['description'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["description"])
        self.assertEqual(json_domain.id,domain.id)
        self.assertEqual(json_domain.name,domain.name)
        self.assertEqual(json_domain.description,domain.description)

    def test_add_domain(self, client):
        resp = client.get('/api/v1/domains')
        self.assertEqual(resp.status_code, 200)
        domain = resp.json['results'][0]
        domain['id'] = 4
        domain['name'] = 'TEST TITLE'
        resp = client.post('/api/v1/domains', json=domain)
        self.assertEqual(resp.status_code, 201)
        resp = client.get('/api/v1/domains/4')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        domain = Domain(4,"TEST TITLE","The courses in the Programming, Data Structures and Algorithms domain teach the knowledge and skills required to design and program solutions to typical information technology problems. The students are taught object-oriented programming in the context of standalone, event-driven and web-based programs.")
        json_domain = Domain(json['id'],json['name'],json['description'])
        self.assertEqual(json_domain.id,domain.id)
        self.assertEqual(json_domain.name,domain.name)
        self.assertEqual(json_domain.description,domain.description)
        

    def test_update_domain(self, client):
        resp = client.get('/api/v1/domains/3')
        self.assertEqual(resp.status_code, 200)
        domain = resp.json
        domain['id'] = 3
        domain['name'] = 'TEST UPDATE TITLE'
        domain['description'] = 'TEST UPDATE TITLE'
        resp = client.patch('/api/v1/domains/3', json=domain)
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/api/v1/domains/3')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        domain = Domain(3,"TEST UPDATE TITLE","TEST UPDATE TITLE")
        json_domain = Domain(json['id'],json['name'],json['description'])
        self.assertEqual(json_domain.id,domain.id)
        self.assertEqual(json_domain.name,domain.name)
        self.assertEqual(json_domain.description,domain.description)

    def test_delete_domain(self, client):
        resp = client.get('/api/v1/domains/3')
        self.assertEqual(resp.status_code, 200)
        domain = resp.json
        resp = client.delete('/api/v1/domains/3', json=domain)
        self.assertEqual(resp.status_code, 204)
    # --------------- END DOMAIN CRUD TEST ---------------

    # --------------- START TERM CRUD TEST ---------------
    def test_get_terms(self, client):
        resp = client.get('/api/v1/terms')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        term = Term(1,"Fall  ")
        json_term = Term(json['results'][0]['id'],json['results'][0]['name'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertEqual(json_term.id,term.id)
        self.assertEqual(json_term.name,term.name)
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_term(self,client):
        resp = client.get('/api/v1/terms/2')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        term = Term(2,"Winter")
        json_term = Term(json['id'],json['name'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])
        self.assertEqual(json_term.id,term.id)
        self.assertEqual(json_term.name,term.name)

    def test_add_term(self, client):
        resp = client.get('/api/v1/terms')
        self.assertEqual(resp.status_code, 200)
        term = resp.json['results'][0]
        term['id'] = 7
        term['name'] = 'Fall  '
        resp = client.post('/api/v1/terms', json=term)
        self.assertEqual(resp.status_code, 201)
        resp = client.get('/api/v1/terms/7')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        term = Term(7,"Fall  ")
        json_term = Term(json['id'],json['name'])
        self.assertEqual(json_term.id,term.id)
        self.assertEqual(json_term.name,term.name)

    def test_update_term(self, client):
        resp = client.get('/api/v1/terms/6')
        self.assertEqual(resp.status_code, 200)
        term = resp.json
        term['id'] = 6
        term['name'] = 'Summer'
        resp = client.patch('/api/v1/terms/6', json=term)
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/api/v1/terms/6')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        term = Term(6,"Summer")
        json_term = Term(json['id'],json['name'])
        self.assertEqual(json_term.id,term.id)
        self.assertEqual(json_term.name,term.name)

    def test_delete_term(self, client):
        resp = client.get('/api/v1/terms/2')
        self.assertEqual(resp.status_code, 200)
        term = resp.json
        resp = client.delete('/api/v1/terms/2', json=term)
        self.assertEqual(resp.status_code, 204)
    # --------------- END TERM CRUD TEST ---------------

    # --------------- START COMPETENCY CRUD TEST ---------------
    def test_get_competencies(self, client):
        resp = client.get('/api/v1/competencies')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_competency(self,client):
        resp = client.get('/api/v1/competencies/00SR')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["achievement"])
        self.assertIsNotNone(json["type"])

    def test_add_competency(self, client):
        resp = client.get('/api/v1/competencies')
        self.assertEqual(resp.status_code, 200)
        competency = resp.json['results'][0]
        competency['id'] = '00XX'
        competency['name'] = 'Understanding te basics of serverside programming'
        competency["achievement"] = '* Based on a problem * Using flask rules'
        competency["type"] = 'Mandatory'
        resp = client.post('/api/v1/competencies', json=competency)
        self.assertEqual(resp.status_code, 201)

    def test_update_competency(self, client):
        resp = client.get('/api/v1/competencies/00SR')
        self.assertEqual(resp.status_code, 200)
        competency = resp.json
        competency['name'] = 'Understanding the basics of flask'
        competency["achievement"] = '* Based on a project * Using refactoring'
        competency["type"] = 'Optional'
        resp = client.patch('/api/v1/competencies/00SR', json=competency)
        self.assertEqual(resp.status_code, 204)

    def test_delete_competency(self, client):
        resp = client.get('/api/v1/competencies/00SR')
        self.assertEqual(resp.status_code, 200)
        competency = resp.json
        resp = client.delete('/api/v1/competencies/00SR', json=competency)
        self.assertEqual(resp.status_code, 204)
    # --------------- END COMPETENCY CRUD TEST ---------------

    # --------------- START ELEMENT OF COMPETENCY CRUD TEST ---------------
    def test_get_elements(self, client):
        resp = client.get('/api/v1/elements')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertIsNotNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_element(self,client):
        resp = client.get('/api/v1/elements/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["order"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["criteria"])
        self.assertIsNotNone(json["competencyId"])
        
    def test_add_element(self, client):
        resp = client.get('/api/v1/elements')
        self.assertEqual(resp.status_code, 200)
        element = resp.json['results'][0]
        element['id'] = '53'
        element['order'] = '3'
        element["name"] = 'Debug flask problems'
        element["criteria"] = '* Correct breakdown of the project * Appropriate choice and adaptation of the framework'
        element["competency_id"] = '00SR'
        resp = client.post('/api/v1/elements', json=element)
        self.assertEqual(resp.status_code, 201)

    def test_update_element(self, client):
        resp = client.get('/api/v1/elements/1')
        self.assertEqual(resp.status_code, 200)
        element = resp.json
        element['order'] = '5'
        element["name"] = 'Debug C# code'
        element["criteria"] = '* Make modular apps* Appropriate team work'
        element["competency_id"] = '00Q8'
        resp = client.patch('/api/v1/elements/1', json=element)
        self.assertEqual(resp.status_code, 204)

    def test_delete_element(self, client):
        resp = client.get('/api/v1/elements/1')
        self.assertEqual(resp.status_code, 200)
        element = resp.json
        resp = client.delete('/api/v1/elements/1', json=element)
        self.assertEqual(resp.status_code, 204)
    # --------------- END ELEMENT OF COMPETENCY CRUD TEST ---------------

    # --------------- START COURSE CRUD TEST ---------------
    def test_get_courses(self, client):
        resp = client.get('/api/v1/courses')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_course(self,client):
        resp = client.get('/api/v1/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["description"])
        self.assertIsNotNone(json["termId"])
        self.assertIsNotNone(json["domainId"])
        self.assertIsNotNone(json["lab_hours"])
        self.assertIsNotNone(json["theory_hours"])
        self.assertIsNotNone(json["work_hours"])
        
    def test_add_course(self, client):
        resp = client.get('/api/v1/courses')
        self.assertEqual(resp.status_code, 200)
        course = resp.json['results'][0]
        course['id'] = '420-620-DE'
        course['name'] = 'Programing VI'
        course["description"] = 'Introduction into advanced development'
        course["term_id"] = '6'
        course["domain_id"] = '2'
        course["lab_hours"] = '3'
        course["theory_hours"] = '4'
        course["work_hours"] = '4'
        resp = client.post('/api/v1/courses', json=course)
        self.assertEqual(resp.status_code, 201)

    def test_update_course(self, client):
        resp = client.get('/api/v1/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)
        course = resp.json
        course['name'] = 'Hacking I'
        course["description"] = 'Introduction to hacking'
        course["term_id"] = '1'
        course["domain_id"] = '1'
        course["lab_hours"] = '5'
        course["theory_hours"] = '5'
        course["work_hours"] = '5'
        resp = client.patch('/api/v1/courses/420-110-DW', json=course)
        self.assertEqual(resp.status_code, 204)

    def test_delete_course(self, client):
        resp = client.get('/api/v1/courses/420-551-D')
        self.assertEqual(resp.status_code, 200)
        course = resp.json
        resp = client.delete('/api/v1/courses/420-551-D', json=course)
        self.assertEqual(resp.status_code, 204)
    # --------------- END COURSE CRUD TEST ---------------

