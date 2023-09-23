from flask import Flask
from app.sqldatabase import db, DB_NAME, create_database
from os import path
from app.app_api import todo_api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
db.init_app(app)


# Register URL handlers
app.register_blueprint(todo_api, url_prefix='/')


if not path.exists('./instance/' + DB_NAME):
    create_database(app)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)