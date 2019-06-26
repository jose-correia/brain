from flask import jsonify, Response, request
from . import bp

import json

# content routes
@bp.route('/')
@bp.route('/', methods=['POST'])
def handlefile():
    return jsonify({'welcome message': "Hi, this is JEEC CV Platform"})


# content routes
@bp.route('/adduser', methods=['POST'])
def add_user():
    return jsonify({'welcome message': "Hi, this is JEEC CV Platform"})


# content routes
@bp.route('/getuser', methods=['GET'])
def get_user():
    return jsonify({'welcome message': "Hi, this is JEEC CV Platform"})


# content routes
@bp.route('/mdeleteusers', methods=['POST', 'DELETE', 'GET'])
def delete_user():
    return jsonify({'welcome message': "Hi, this is JEEC CV Platform"})

    
@bp.route('/cleantemporary', methods=['GET'])
def get():
    return jsonify({'welcome message': "Hi, this is JEEC CV Platform"})

