from app import app,db
from flask import jsonify, request
from models import User, Post, Comments
from werkzeug.exceptions import BadRequest, NotFound
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

@app.route('/v1/posts', methods=['GET'])
def get_posts():
  posts = Post.query.all()
  return jsonify(posts=[p.to_dict() for p in posts]), 200

@app.route('/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
  post = Post.query.allget(post_id)
  if not post:
    raise NotFound('Post not found')
  return jsonify(post=post.to_dict()), 200


@app.route('/v1/posts/<int:post_id>', methods=['PATCH'])
@jwt_required()
def update_post(post_id):
  user_id = get_jwt_identity()
  post = Post.query.get(post_id)
  if not post:
    raise NotFound('Post not found')
  if post.author_id != user_id:
    return jsonify(message='Unauthorized'), 403
  data = request.get_json()
  post.title = data.get('title', post.title)
  post.body = data.get('body', post.body)
  db.session.commit()
  return jsonify(message='Post updated'), 200


@app.route('/v1/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
  user_id = get_jwt_identity()
  post = Post.query.get(post_id)
  if not post:
    raise NotFound('Post not found')
  if post.author_id != user_id:
    return jsonify(message='Unauthorized'), 403
  db.session.delete(post)
  db.session.commit()
  return jsonify(message='Post deleted'), 200



@app.route('/v1/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
  user_id = get_jwt_identity()
  post = Post.query.get(post_id)
  if not post:
    raise NotFound('Post not found')
  data = request.get_json()
  body = data.get('body')
  if not body:
    raise BadRequest('Comment body is required')
  comment = Comments(body=body, author_id=user_id, post_id=post_id)
  db.session.add(comment)
  db.session.commit()
  return jsonify(message='Comment added'), 201


@app.route('/v1/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
  post = Post.query.get(post_id)
  if not post:
    raise NotFound('Post not found')
  comments = Comments.query.filter_by(post_id=post_id).all()
  return jsonify(comments=[c.to_dict() for c in comments]), 200