from app import app
from flask import jsonify
@app.route('/', methods=['GET'])
def home():
  return jsonify(message="Welcome to the Flask API!")