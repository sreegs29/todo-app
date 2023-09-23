from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_NAME = 'database.db'
engine = create_engine(f"sqlite:///{DB_NAME}")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

db = SQLAlchemy(model_class=Base)


def create_database(app):
    with app.app_context():
        db.create_all()
        print('Database created successfully!')

