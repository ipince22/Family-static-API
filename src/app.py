"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get All Members
@app.route('/members', methods=['GET'])
def get_all_members():

    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

# Get Single Member
@app.route('/member/<int:id>', methods=["GET"])
def get_member(id):

    member = jackson_family.get_member(id)
    response_body = {
        "name": f"{member['first_name']} {member['last_name']}",
        "id": member['id'],
        "age": member['age'],
        "lucky_numbers": member['lucky_numbers']
    }
    return jsonify(response_body), 200

# Create Member
@app.route('/member', methods=['POST'])
def create_member():
    member = request.json

    check_if_exists = list(filter(lambda x: x['id'] == member['id'], jackson_family.get_all_members()))
    if len(check_if_exists) > 0:
        return jsonify({'error': 'Member already exists'}), 401

    jackson_family.add_member(member)
    response_body = {}
    return jsonify(response_body), 200

# Delete Member
@app.route('/member/<int:id>', methods=["DELETE"])
def delete_member(id):

    check_if_exists = list(filter(lambda member: member['id'] == id, jackson_family.get_all_members()))
    if not (len(check_if_exists) > 0):
        return jsonify({'error': 'Member to delete does not exist'}), 401
    
    jackson_family.delete_member(id)
    body = {"done": "True"} 
    return jsonify(body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
