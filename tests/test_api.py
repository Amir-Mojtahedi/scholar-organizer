import flask_unittest
from CoursePlannerApp import create_app
from CoursePlannerApp.objects.competency import Competency
from CoursePlannerApp.objects.course import Course
from CoursePlannerApp.objects.domain import Domain
from CoursePlannerApp.objects.element import Element
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
        domain['name'] = 'TEST UPDATE TITLE'
        domain['description'] = 'TEST UPDATE TITLE'
        resp = client.put('/api/v1/domains/3', json=domain)
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
        resp = client.delete('/api/v1/domains/2')
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
        term['name'] = 'Summer'
        resp = client.put('/api/v1/terms/6', json=term)
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/api/v1/terms/6')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        term = Term(6,"Summer")
        json_term = Term(json['id'],json['name'])
        self.assertEqual(json_term.id,term.id)
        self.assertEqual(json_term.name,term.name)

    def test_delete_term(self, client):
        resp = client.delete('/api/v1/terms/3')
        self.assertEqual(resp.status_code, 204)
    # --------------- END TERM CRUD TEST ---------------

    # --------------- START COMPETENCY CRUD TEST ---------------
    def test_get_competencies(self, client):
        resp = client.get('/api/v1/competencies')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        competency = Competency("00Q2","Use programming languages","* For problems that are easily solved * Using basic algorithms * Using a debugger and a functional test plan","Mandatory")
        json_competency = Competency(json['results'][1]['id'],json['results'][1]['name'],json['results'][1]['achievement'],json['results'][1]['type'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertEqual(json_competency.id,competency.id)
        self.assertEqual(json_competency.name,competency.name)
        self.assertEqual(json_competency.achievement,competency.achievement)
        self.assertEqual(json_competency.type,competency.type)
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_competency(self,client):
        resp = client.get('/api/v1/competencies/00Q2')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        competency = Competency("00Q2","Use programming languages","* For problems that are easily solved * Using basic algorithms * Using a debugger and a functional test plan","Mandatory")
        json_competency = Competency(json['id'],json['name'],json['achievement'],json['type'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["achievement"])
        self.assertIsNotNone(json["type"])
        self.assertEqual(json_competency.id,competency.id)
        self.assertEqual(json_competency.name,competency.name)
        self.assertEqual(json_competency.achievement,competency.achievement)
        self.assertEqual(json_competency.type,competency.type)

    def test_add_competency(self, client):
        resp = client.get('/api/v1/competencies')
        self.assertEqual(resp.status_code, 200)
        competency = resp.json['results'][0]
        competency['id'] = '00XX'
        competency['name'] = 'Understanding the basics of serverside programming'
        competency["achievement"] = '* Based on a problem * Using flask rules'
        competency["type"] = 'Mandatory'
        resp = client.post('/api/v1/competencies', json=competency)
        self.assertEqual(resp.status_code, 201)
        resp = client.get('/api/v1/competencies/00XX')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        competency = Competency("00XX","Understanding the basics of serverside programming",'* Based on a problem * Using flask rules',"Mandatory")
        json_competency = Competency(json['id'],json['name'],json['achievement'],json['type'])
        self.assertEqual(json_competency.id,competency.id)
        self.assertEqual(json_competency.name,competency.name)
        self.assertEqual(json_competency.achievement,competency.achievement)
        self.assertEqual(json_competency.type,competency.type)

    def test_update_competency(self, client):
        resp = client.get('/api/v1/competencies/00SR')
        self.assertEqual(resp.status_code, 200)
        competency = resp.json
        competency['name'] = 'Understanding the basics of flask'
        competency["achievement"] = '* Based on a project * Using refactoring'
        competency["type"] = 'Optional'
        resp = client.put('/api/v1/competencies/00SR', json=competency)
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/api/v1/competencies/00SR')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        competency = Competency("00SR","Understanding the basics of flask","* Based on a project * Using refactoring","Optional")
        json_competency = Competency(json['id'],json['name'],json['achievement'],json['type'])
        self.assertEqual(json_competency.id,competency.id)
        self.assertEqual(json_competency.name,competency.name)
        self.assertEqual(json_competency.achievement,competency.achievement)
        self.assertEqual(json_competency.type,competency.type)

    def test_delete_competency(self, client):
        resp = client.delete('/api/v1/competencies/00SS')
        self.assertEqual(resp.status_code, 204)
    # --------------- END COMPETENCY CRUD TEST ---------------

    # --------------- START ELEMENT OF COMPETENCY CRUD TEST ---------------
    def test_get_elements(self, client):
        resp = client.get('/api/v1/elements')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        element = Element(1,1,"Analyze the problem.","* Correct breakdown of the problem * Proper identification of input and output data and of the nature of the processes * Appropriate choice and adaptation of the algorithm","00Q2")
        json_element = Element(json['results'][0]['id'],json['results'][0]['order'],json['results'][0]['name'],json['results'][0]['criteria'],json['results'][0]['competencyId'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertEqual(json_element.id,element.id)
        self.assertEqual(json_element.order,element.order)
        self.assertEqual(json_element.name,element.name)
        self.assertEqual(json_element.criteria,element.criteria)
        self.assertEqual(json_element.competencyId,element.competencyId)
        self.assertIsNotNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_element(self,client):
        resp = client.get('/api/v1/elements/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        element = Element(1,1,"Analyze the problem.","* Correct breakdown of the problem * Proper identification of input and output data and of the nature of the processes * Appropriate choice and adaptation of the algorithm","00Q2")
        json_element = Element(json['id'],json['order'],json['name'],json['criteria'],json['competencyId'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["order"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["criteria"])
        self.assertIsNotNone(json["competencyId"])
        self.assertEqual(json_element.id,element.id)
        self.assertEqual(json_element.order,element.order)
        self.assertEqual(json_element.name,element.name)
        self.assertEqual(json_element.criteria,element.criteria)
        self.assertEqual(json_element.competencyId,element.competencyId)
        
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
        element['order'] = 5
        element["name"] = 'Debug C# code'
        element["criteria"] = '* Make modular apps* Appropriate team work'
        element["competency_id"] = '00Q8'
        resp = client.put('/api/v1/elements/1', json=element)
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/api/v1/elements/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        element = Element(1,5,"Debug C# code","* Make modular apps* Appropriate team work","00Q8")
        json_element = Element(json['id'],json['order'],json['name'],json['criteria'],json['competencyId'])
        self.assertEqual(json_element.id,element.id)
        self.assertEqual(json_element.order,element.order)
        self.assertEqual(json_element.name,element.name)
        self.assertEqual(json_element.criteria,element.criteria)
        self.assertEqual(json_element.competencyId,element.competencyId)

    def test_delete_element(self, client):
        resp = client.delete('/api/v1/elements/2')
        self.assertEqual(resp.status_code, 204)
    # --------------- END ELEMENT OF COMPETENCY CRUD TEST ---------------

    # --------------- START COURSE CRUD TEST ---------------
    def test_get_courses(self, client):
        resp = client.get('/api/v1/courses')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        course = Course("420-110-DW","Programming I","The course will introduce the student to the basic building blocks (sequential, selection and repetitive control structures) and modules (methods and classes) used to write a program. The student will use the Java programming language to implement the algorithms studied. The array data structure is introduced, and student will learn how to program with objects.",1,1,3,3,3)
        json_course = Course(json['results'][0]['id'],json['results'][0]['name'],json['results'][0]['description'],json['results'][0]['termId'],json['results'][0]['domainId'],json['results'][0]['lab_hours'],json['results'][0]['theory_hours'],json['results'][0]['work_hours'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])
        self.assertEqual(json_course.id,course.id)
        self.assertEqual(json_course.name,course.name)
        self.assertEqual(json_course.description,course.description)
        self.assertEqual(json_course.termId,course.termId)
        self.assertEqual(json_course.domainId,course.domainId)
        self.assertEqual(json_course.lab_hours,course.lab_hours)
        self.assertEqual(json_course.theory_hours,course.theory_hours)
        self.assertEqual(json_course.work_hours,course.work_hours)

    def test_get_course(self,client):
        resp = client.get('/api/v1/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        course = Course("420-110-DW","Programming I","The course will introduce the student to the basic building blocks (sequential, selection and repetitive control structures) and modules (methods and classes) used to write a program. The student will use the Java programming language to implement the algorithms studied. The array data structure is introduced, and student will learn how to program with objects.",1,1,3,3,3)
        json_course = Course(json['id'],json['name'],json['description'],json['termId'],json['domainId'],json['lab_hours'],json['theory_hours'],json['work_hours'])
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["description"])
        self.assertIsNotNone(json["termId"])
        self.assertIsNotNone(json["domainId"])
        self.assertIsNotNone(json["lab_hours"])
        self.assertIsNotNone(json["theory_hours"])
        self.assertIsNotNone(json["work_hours"])
        self.assertEqual(json_course.name,course.name)
        self.assertEqual(json_course.description,course.description)
        self.assertEqual(json_course.termId,course.termId)
        self.assertEqual(json_course.domainId,course.domainId)
        self.assertEqual(json_course.lab_hours,course.lab_hours)
        self.assertEqual(json_course.theory_hours,course.theory_hours)
        self.assertEqual(json_course.work_hours,course.work_hours)
        
    def test_add_course(self, client):
        resp = client.get('/api/v1/courses')
        self.assertEqual(resp.status_code, 200)
        course = resp.json['results'][0]
        course['id'] = '420-620-DE'
        course['name'] = 'Programing VI'
        course["description"] = 'Introduction to advanced development'
        course["term_id"] = '6'
        course["domain_id"] = '2'
        course["lab_hours"] = 3
        course["theory_hours"] = 4
        course["work_hours"] = 4
        resp = client.post('/api/v1/courses', json=course)
        self.assertEqual(resp.status_code, 201)
        resp = client.get('/api/v1/courses/420-620-DE')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        course = Course("420-620-DE","Programing VI","Introduction to advanced development",6,2,3,4,4)
        json_course = Course(json['id'],json['name'],json['description'],json['termId'],json['domainId'],json['lab_hours'],json['theory_hours'],json['work_hours'])
        self.assertEqual(json_course.name,course.name)
        self.assertEqual(json_course.description,course.description)
        self.assertEqual(json_course.termId,course.termId)
        self.assertEqual(json_course.domainId,course.domainId)
        self.assertEqual(json_course.lab_hours,course.lab_hours)
        self.assertEqual(json_course.theory_hours,course.theory_hours)
        self.assertEqual(json_course.work_hours,course.work_hours)

    def test_update_course(self, client):
        resp = client.get('/api/v1/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)
        course = resp.json
        course['name'] = 'Hacking I'
        course["description"] = 'Introduction to hacking'
        course["term_id"] = '1'
        course["domain_id"] = '1'
        course["lab_hours"] = 5
        course["theory_hours"] = 5
        course["work_hours"] = 5
        resp = client.put('/api/v1/courses/420-110-DW', json=course)
        self.assertEqual(resp.status_code, 204)
        resp = client.get('/api/v1/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        course = Course("420-110-DW","Hacking I","Introduction to hacking",1,1,5,5,5)
        json_course = Course(json['id'],json['name'],json['description'],json['termId'],json['domainId'],json['lab_hours'],json['theory_hours'],json['work_hours'])
        self.assertEqual(json_course.name,course.name)
        self.assertEqual(json_course.description,course.description)
        self.assertEqual(json_course.termId,course.termId)
        self.assertEqual(json_course.domainId,course.domainId)
        self.assertEqual(json_course.lab_hours,course.lab_hours)
        self.assertEqual(json_course.theory_hours,course.theory_hours)
        self.assertEqual(json_course.work_hours,course.work_hours)

    def test_delete_course(self, client):
        resp = client.delete('/api/v1/courses/420-551-D')
        self.assertEqual(resp.status_code, 204)
    # --------------- END COURSE CRUD TEST ---------------

    # --------------- START COURSE EXCEPTION TEST ---------------
    def test_get_course_404(self,client):
        resp = client.get('/api/v1/courses/720-110-DW')
        self.assertEqual(resp.status_code, 404)
        
    def test_add_course_400(self, client):
        resp = client.get('/api/v1/courses')
        self.assertEqual(resp.status_code, 200)
        course = resp.json['results'][0]
        course['id'] = '420-620-DE'
        course['name'] = 'Programing VI'
        course["description"] = 'Introduction to advanced development'
        course["term_id"] = '6'
        resp = client.post('/api/v1/courses', json=course)
        self.assertEqual(resp.status_code, 400)

    def test_update_course_400(self, client):
        resp = client.get('/api/v1/courses/420-110-DW')
        self.assertEqual(resp.status_code, 200)
        course = resp.json
        course['name'] = 'Hacking I'
        course["description"] = 'Introduction to hacking'
        course["term_id"] = '1'
        resp = client.put('/api/v1/courses/420-110-DW', json=course)
        self.assertEqual(resp.status_code, 400)
    # --------------- END COURSE EXCEPTION TEST ---------------
    

