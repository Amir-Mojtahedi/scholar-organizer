import flask_unittest
from CoursePlannerApp import create_app

class TestForAPI(flask_unittest.ClientTestCase):
    app = create_app()

    def test_get_domains(self, client):
        resp = client.get('/api/posts')
        self.assertEqual(resp.status_code, 200)
        json = resp.json
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['results'])
        self.assertIsNotNone(json['next_page'])
        self.assertIsNone(json['prev_page'])

    def test_post_domain(self, client):
        resp = client.get('/api/posts')
        post = resp.json['results'][0]

        post['title'] = 'TEST TITLE'
        resp = client.post('/api/posts', json=post)
        self.assertEqual(resp.status_code, 201)
