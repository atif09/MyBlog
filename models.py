from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True) #since it is going to be unique
  username = db.Column(db.String(64), unique=True, index=True)
  email = db.Column(db.String(120), unique=True, index=True) 
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref='author', lazy='dynamic') #lazy parameter to dynamic helps in increasing performance

  def set_password(self,password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  @classmethod
  def authenticate(cls, email,password):
    user = cls.query.filter_by(email=email).first()
    if user and user.check_password(password):
      access_token = create_access_token(identity=user.id)
      return access_token, user

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(140))
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'))



