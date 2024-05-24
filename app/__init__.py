from flask import Flask
from flask_restful import Api
from app.extensions import db, migrate
from app.resources.tasks import TasksListResource, TaskResource

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    api.add_resource(TaskResource, '/tasks/<int:task_id>')
    api.add_resource(TasksListResource, '/tasks')
    
    return app