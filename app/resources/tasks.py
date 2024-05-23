from flask import abort
from flask_restful import Resource, fields, marshal_with, reqparse

from app.models import Task
from app.extensions import db


task_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
parser.add_argument('description', type=str, required=False)

put_parser = reqparse.RequestParser()
put_parser.add_argument('title', type=str, required=False)
put_parser.add_argument('description', type=str, required=False)


class TasksListResource(Resource):
    @marshal_with(task_fields)
    def get(self):
        tasks = Task.query.all()
        return tasks

    @marshal_with(task_fields)
    def post(self):
        args = parser.parse_args()
        new_task = Task(
            title=args['title'],
            description=args['description']
        )

        db.session.add(new_task)
        db.session.commit()

        return new_task, 201


class TaskResource(Resource):
    @marshal_with(task_fields)
    def get(self, task_id):
        return Task.query.get_or_404(task_id)
        
    @marshal_with(task_fields)
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

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {'message': f'Task {task_id} successfully deleted.'}, 200