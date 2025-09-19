
#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
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

# -----------------------
# ROUTES
# -----------------------

@app.route('/')
def index():
    return {"message": "Chatterbox API is running!"}


# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([m.to_dict() for m in messages])


# GET one message by ID
@app.route('/messages/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_dict())


# CREATE a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or not data.get("body") or not data.get("username"):
        return make_response({"error": "Invalid input"}, 400)

    new_message = Message(
        body=data["body"],
        username=data["username"],
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201


# UPDATE a message by ID
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if "body" in data:
        message.body = data["body"]
    if "username" in data:
        message.username = data["username"]

    db.session.commit()
    return jsonify(message.to_dict())


# DELETE a message by ID
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return make_response({}, 204)


# -----------------------
# MAIN
# -----------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)
