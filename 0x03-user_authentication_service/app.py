#!/usr/bin/env python3
""" basic Flask app """
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def root_path():
    """ Root path
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ users POST request to create a new user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ sessions POST to login a user """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        res = jsonify({"email": "{}".format(email), "message": "logged in"})
        sessionID = AUTH.create_session(email)
        res.set_cookie("session_id", sessionID)
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ sessions DELETE to logout a user """
    sessionID = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=sessionID)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ profile GET to find a user"""
    sessionID = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=sessionID)
    if user:
        return jsonify({"email": "{}".format(user.email)}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        data = {"email": "{}".format(email), "reset_token": "{}".format(token)}
        return jsonify(data), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
