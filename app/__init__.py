from flask import Flask
from flask_restx import Api

from app.extensions import db, migrate
from app.resources.tasks import tasks_api


def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app, version='1.0', title='Task API', description='Simple TODO List.', doc='/api-docs/')

    api.add_namespace(tasks_api, path='/tasks')
    
    return app