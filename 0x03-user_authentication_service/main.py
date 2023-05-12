#!/usr/bin/env python3
"""
Main file
"""
import requests


url = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """ register a new user """
    path = "{}/users".format(url)
    data = {"email": email, "password": password}
    response = requests.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ wrong password login """
    path = "{}/sessions".format(url)
    data = {"email": email, "password": password}
    response = requests.post(path, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Real user login """
    path = "{}/sessions".format(url)
    data = {"email": email, "password": password}
    response = requests.post(path, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """ unlogged profile access """
    path = "{}/profile".format(url)
    response = requests.get(path)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ logged profile access """
    path = "{}/profile".format(url)
    response = requests.get(path, cookies={"session_id": session_id})
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """ loggin out a user """
    path = "{}/sessions".format(url)
    response = requests.delete(path, cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """ request a reset ppassword token """
    path = "{}/reset_password".format(url)
    data = {"email": email}
    response = requests.post(path, data)
    assert response.status_code == 200
    # print(response.json()["reset_token"])
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update password """
    path = "{}/reset_password".format(url)
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(path, data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
