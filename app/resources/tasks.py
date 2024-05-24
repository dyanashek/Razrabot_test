from flask import abort
from flask_restx import Namespace, Resource, reqparse, fields

from app.models import Task
from app.extensions import db


tasks_api = Namespace('Tasks', description='Task operations')

task_fields = tasks_api.model('Task', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
})

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
parser.add_argument('description', type=str, required=False)

put_parser = reqparse.RequestParser()
put_parser.add_argument('title', type=str, required=False)
put_parser.add_argument('description', type=str, required=False)


@tasks_api.route('/')
class TasksListResource(Resource):
    @tasks_api.marshal_with(task_fields)
    @tasks_api.doc(description='Get tasks list.')
    def get(self):
        tasks = Task.query.all()
        return tasks

    @tasks_api.marshal_with(task_fields, code=201)
    @tasks_api.expect(parser)
    @tasks_api.doc(description='Create a task.', responses={400: 'Bad request.'})
    def post(self):
        args = parser.parse_args()
        new_task = Task(
            title=args['title'],
            description=args['description']
        )

        db.session.add(new_task)
        db.session.commit()

        return new_task, 201


@tasks_api.route('/<int:task_id>/')
@tasks_api.response(404, 'Task not found')
@tasks_api.param('task_id', 'The task identifier')
class TaskResource(Resource):
    @tasks_api.marshal_with(task_fields)
    @tasks_api.doc(description='Get a task by ID.')
    def get(self, task_id):
        return Task.query.get_or_404(task_id)
        
    @tasks_api.marshal_with(task_fields)
    @tasks_api.expect(put_parser)
    @tasks_api.doc(description="Update task's title/description by ID.", responses={400: 'Bad request.'})
    def put(self, task_id):
        args = put_parser.parse_args()

        task = Task.query.get_or_404(task_id)
        title = args.get('title')
        description = args.get('description')

        if title or description:
            if title:
                task.title = title
            if description:
                task.description = description

            db.session.commit()

            return task
        else:
            abort(400, 'At least one of the fields (title or description) is required.')

    @tasks_api.doc(description='Delete task by ID.', responses={200: 'Task deleted.'})
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {'message': f'Task {task_id} successfully deleted.'}, 200