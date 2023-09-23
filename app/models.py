from .sqldatabase import db
from sqlalchemy.sql import func


class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  

