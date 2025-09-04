from app import app,db
from flask import jsonify, request
from models import User
from werkzeug.exceptions import BadRequest


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
