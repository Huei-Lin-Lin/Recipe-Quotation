from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .db import MyDB


load_dotenv()
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
db_name = os.getenv('DB_NAME')

db = MyDB(user, password, host, port, db_name)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'My flask project!'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.init_app(app)

    with app.app_context():
        db.cursor = db.connect()

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
