from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        messages_serialized = [message.to_dict() for message in messages]
        response = make_response(
            jsonify(messages_serialized),
            200
        )

    elif request.method == 'POST':
        message = Message(
            body=request.get_json()['body'],
            username=request.get_json()['username']
        )
        message_serialized = message.to_dict()

        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message_serialized),
            201,
        )

    return response
    

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'GET':
        message_serialized = message.to_dict()
        response = make_response(
            jsonify(message_serialized),
            200
        )

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response = make_response(
            jsonify({"success": "message deleted"}),
            200
        )

    elif request.method == 'PATCH':
        data = request.get_json()
        for field in data:
            setattr(message, field, data[field])
            
        db.session.add(message)
        db.session.commit()

        message_serialized = message.to_dict()

        response = make_response(
            jsonify(message_serialized),
            200,
        )

    return response

if __name__ == '__main__':
    app.run(port=5555)
