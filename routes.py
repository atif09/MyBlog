from app import app,db
from flask import jsonify, request
from models import User, Post
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/', methods=['GET'])
def home():
  return jsonify(message="Welcome to the Flask API")


@app.route('/v1/register', methods=['POST'])
def register():
  data = request.get_json()
  if not data:
    return {'message': 'No input data provided'}, 400
  
  email = data.get('email')
  username = data.get('username')
  password = data.get('password')
  if not email or not username or not password: 
    return {'message': 'Missing required fields'}, 400
  
  user = User(email=email, username=username)
  user.set_password(password)
  db.session.add(user)
  db.session.commit()
  return jsonify(message='Successful'), 201

@app.route('/v1/login', methods=['POST'])
def login():
  data = request.get_json()
  if not data: #diff approach to raise error
    raise BadRequest('Invalid data')
  
  email = data.get('email')
  password = data.get('password')

  token, _= User.authenticate(email, password)
  if not token:
    raise BadRequest('Invalid credentials')
  return jsonify(access_token=token), 200

@app.route('/v1/posts', methods=['POST'])
#protect this route
@jwt_required()
def add_post():
  user_id = get_jwt_identity()
  data = request.get_json()
  title = data.get('title')
  body = data.get('body')
  if not title or not body:
    raise BadRequest('Title and body are required')
  post = Post(title=title, body=body, author_id=user_id)
  db.session.add(post)
  db.session.commit()
  return jsonify(message='Post created'), 201
