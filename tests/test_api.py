import flask_unittest
from CoursePlannerApp import create_app

class TestForAPI(flask_unittest.ClientTestCase):
    app = create_app()

    def test_get_domains(self, client):
        resp = client.get('/api/v1/domains')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['results'])
        self.assertIsNone(json['next'])
        self.assertIsNone(json['prev'])

    def test_add_domain(self, client):
        resp = client.get('/api/v1/domains')
        domain = resp.json['results'][0]

        domain['id'] = 4
        domain['name'] = 'TEST TITLE'
        resp = client.post('/api/v1/domains', json=domain)
        self.assertEqual(resp.status_code, 201)
