from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)



@app.cli.command('db_create')
def db_create():
  db.create_all()
  print("Database created")
  









import routes 