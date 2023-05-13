import unittest
import json
from app import app, db
from app.models.user import User
from app.models.post import Post

class PosterrBackendTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alvarosps:sps@localhost/test_posterr'
        self.client = app.test_client()
        db.create_all()

        self.user = User(username='testuser')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_post(self):
        response = self.client.post('/api/posts', json={
            "user_id": self.user.id,
            "content": "Test post content"
        })

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["content"], "Test post content")
        self.assertEqual(data["user_id"], self.user.id)
        self.assertIsNone(data["repost_id"])

if __name__ == '__main__':
    unittest.main()