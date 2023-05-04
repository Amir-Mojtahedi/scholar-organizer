import flask_unittest
from CoursePlannerApp import create_app

class TestForAPI(flask_unittest.ClientTestCase):
    app = create_app()

    # --------------- START DOMAIN CRUD TEST ---------------
    def test_get_domains(self, client):
        resp = client.get('/api/v1/domains')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_domain(self,client):
        resp = client.get('/api/v1/domains/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])
        self.assertIsNotNone(json["description"])

    def test_add_domain(self, client):
        resp = client.get('/api/v1/domains')
        self.assertEqual(resp.status_code, 200)
        domain = resp.json['results'][0]
        domain['id'] = 4
        domain['name'] = 'TEST TITLE'
        resp = client.post('/api/v1/domains', json=domain)
        self.assertEqual(resp.status_code, 201)

    def test_update_domain(self, client):
        resp = client.get('/api/v1/domains/4')
        self.assertEqual(resp.status_code, 200)
        domain = resp.json
        domain['id'] = 4
        domain['name'] = 'TEST UPDATE TITLE'
        domain['description'] = 'TEST UPDATE DESCRIPTION'
        resp = client.patch('/api/v1/domains/4', json=domain)
        self.assertEqual(resp.status_code, 204)

    def test_delete_domain(self, client):
        resp = client.get('/api/v1/domains/4')
        self.assertEqual(resp.status_code, 200)
        domain = resp.json
        resp = client.delete('/api/v1/domains/4', json=domain)
        self.assertEqual(resp.status_code, 204)
    # --------------- END DOMAIN CRUD TEST ---------------

    # --------------- START TERM CRUD TEST ---------------
    def test_get_terms(self, client):
        resp = client.get('/api/v1/terms')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['count'])
        self.assertIsNotNone(json['results'])
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_get_term(self,client):
        resp = client.get('/api/v1/terms/1')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json["id"])
        self.assertIsNotNone(json["name"])

    def test_add_term(self, client):
        resp = client.get('/api/v1/terms')
        self.assertEqual(resp.status_code, 200)
        term = resp.json['results'][0]
        term['id'] = 7
        term['name'] = 'FALL'
        resp = client.post('/api/v1/terms', json=term)
        self.assertEqual(resp.status_code, 201)

    def test_update_term(self, client):
        resp = client.get('/api/v1/terms/7')
        self.assertEqual(resp.status_code, 200)
        term = resp.json
        term['id'] = 7
        term['name'] = 'FALL'
        resp = client.patch('/api/v1/terms/7', json=term)
        self.assertEqual(resp.status_code, 204)

    def test_delete_term(self, client):
        resp = client.get('/api/v1/terms/7')
        self.assertEqual(resp.status_code, 200)
        term = resp.json
        resp = client.delete('/api/v1/terms/7', json=term)
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
        resp = client.get('/api/v1/competencies/00XX')
        self.assertEqual(resp.status_code, 200)
        competency = resp.json
        competency['name'] = 'Understanding te basics of flask'
        competency["achievement"] = '* Based on a project * Using refactoring'
        competency["type"] = 'Optional'
        resp = client.patch('/api/v1/competencies/00XX', json=competency)
        self.assertEqual(resp.status_code, 204)

        resp = client.get('/api/v1/competencies/00XX')
        self.assertEqual(resp.status_code, 200)
        competency = resp.json
        resp = client.delete('/api/v1/competencies/00XX', json=competency)
        self.assertEqual(resp.status_code, 204)
    # --------------- END COMPETENCY CRUD TEST ---------------

    # --------------- START ELEMENT OF COMPETENCY CRUD TEST ---------------
    # --------------- END ELEMENT OF COMPETENCY CRUD TEST ---------------

    # --------------- START COURSE CRUD TEST ---------------
    # --------------- END COURSE CRUD TEST ---------------

