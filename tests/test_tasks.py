import unittest
import time

from app import create_app, db
from app.models import Task


class TaskCRUTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('app.config.TestConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            new_task = Task(
                title='test_init_title',
                description='test_init_description',
            )

            db.session.add(new_task)
            db.session.commit()

    def test_create_task_invalid_data(self):
        response = self.client.post('/tasks', json={
            'description': 'Test description'
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_task(self):
        response = self.client.post('/tasks', json={
            'title': 'Test title',
            'description': 'Test description',
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data.get('title'), 'Test title')
        self.assertEqual(data.get('description'), 'Test description')
        self.assertEqual(data.get('created_at'), data.get('updated_at'))
        task_id = data.get('id')

        with self.app.app_context():
            self.assertIsInstance(Task.query.filter_by(id=task_id).first(), Task)
    
    def test_get_tasks_list(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.get_json()), 0)
    
    def test_get_wrong_task(self):
        response = self.client.get('/tasks/3')
        self.assertEqual(response.status_code, 404)
    
    def test_get_task(self):
        response = self.client.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('id'), 1)
    
    def test_update_task_with_invalid_data(self):
        response = self.client.put('/tasks/1', json={
            'unknown_field': 'value',
        })
        self.assertEqual(response.status_code, 400)

    def test_update_task(self):
        time.sleep(1)
        response = self.client.put('/tasks/1', json={
            'title': 'updated_title',
            'description': 'updated_description',
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('title'), 'updated_title')
        self.assertEqual(data.get('description'), 'updated_description')
        self.assertNotEqual(data.get('created_at'), data.get('updated_at'))
        with self.app.app_context():
            task = Task.query.filter_by(id=1).first()
            self.assertNotEqual(task.created_at, task.updated_at)
            self.assertEqual(task.title, 'updated_title')
            self.assertEqual(task.description, 'updated_description')
        
    def test_delete_wrong_task(self):
        response = self.client.delete('/tasks/3')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class TaskDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('app.config.TestConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            new_task = Task(
                title='test_init_title',
                description='test_init_description',
            )

            db.session.add(new_task)
            db.session.commit()
    
    def test_delete_task(self):
        response = self.client.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertIs(Task.query.filter_by(id=1).first(), None)
        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
