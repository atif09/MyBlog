class Config:
  SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
  import os
  from dotenv import load_dotenv
  load_dotenv()
  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')