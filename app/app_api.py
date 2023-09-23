from flask_restful import reqparse, abort, fields, marshal_with
from flask import Blueprint, request
from .models import Todo
from .sqldatabase import db


todo_api = Blueprint('todo_api', __name__)


# Serializing the data.
required_fields = {
    'id': fields.Integer,
    'note': fields.String,
    'date': fields.DateTime
}


@todo_api.route('/todos', methods=['GET'])
@marshal_with(required_fields)
def get_todo():
    todos = Todo.query.all()
    if not todos:
        abort(404, details="Todo list not found.")
    return todos, 200


@todo_api.route('/add_todo', methods=['POST'])
def post_todo():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('note', type=str, help="Add some notes.", required=True)
        args = parser.parse_args()
        
        if len(args['note']) < 1:
            return 'Please add some notes', 409
        else:
            todo = Todo(note=args['note'])
            db.session.add(todo)
            db.session.commit()
            return '', 201
        

@todo_api.route('/update_todo/<int:noteid>', methods=['PATCH'])
def update_note(noteid):
    todo = Todo.query.filter_by(id=noteid).first()
    if not todo:
        return 'Todo not found', 404
    else:
        parser = reqparse.RequestParser()
        parser.add_argument('note', type=str, help="Add some notes.", required=True)
        args = parser.parse_args()

        if len(args['note']) < 1:
            return 'Please add some notes', 409
        else:
            todo.note = args['note']
            db.session.commit()
            return '', 204


@todo_api.route('/delete_todo/<int:noteid>', methods=['DELETE'])
def delete_note(noteid):
    todo = Todo.query.filter_by(id=noteid).first()
    if not todo:
        return 'Todo not found', 404
    else:
        db.session.delete(todo)
        db.session.commit()
        return '', 204


@todo_api.route('/todo_bulk', methods=['POST'])
def create_bulk_todos():
    if request.method == 'POST':
        parser = reqparse.RequestParser()
        parser.add_argument('todo', type=list, location='json', help="Add some notes.", required=True)
        args = parser.parse_args()

        # print(args)
        # {'todo': [{'note': 'Bulk post Todo 1'}, {'note': 'Bulk post Todo 2'}]}
        todo_lst = args['todo']

        if len(todo_lst) < 1:
            return 'Empty post.', 409
        else:
            for todo in todo_lst:
                if len(todo['note']) < 1:
                    return 'Please add some notes', 409
                blk_todo = Todo(note=todo['note'])
                db.session.add(blk_todo)
                db.session.commit()
        return '', 201
        
