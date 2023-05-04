#!/usr/bin/env python3
""" Module of session_auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_session(email: str = None, password: str = None) -> str:
    """ Route to create new session for a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return jsonify({'error': "email missing"}), 400
    if password is None:
        return jsonify({'error': "password missing"}), 400

    result = User.search({'email': email})
    for user in result:
        if user:
            if user.is_valid_password(password):
                from api.v1.app import auth
                sessionId = auth.create_session(user.id)
                respons = jsonify(user.to_json())
                SESSION_NAME = os.getenv('SESSION_NAME')
                respons.set_cookie(SESSION_NAME, sessionId)
                return respons

            else:
                return jsonify({"error": "wrong password"}), 401

    return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_session() -> str:
    """Route to delete a session for a user"""
    from api.v1.app import auth
    try:
        auth.destroy_session(request)
        return jsonify({}), 200
    except Exception:
        abort(404)
