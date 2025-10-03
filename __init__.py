from flask import Flask
from my_project.db_init import db


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Maks_mia3@localhost/database_lab1_eer'

    db.init_app(app)

    return app
