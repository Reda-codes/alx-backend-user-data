#!/usr/bin/env paython3
"""
Main file
"""
import requests


url = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """ register a new user """
    data = {"email": email, "password": password}
    response = requests.post("{}/users".format(url), data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ wrong password login """
    pass


def log_in(email: str, password: str) -> str:
    """ Real user login """
    pass


def profile_unlogged() -> None:
    """ unlogged profile access """
    pass


def profile_logged(session_id: str) -> None:
    """ logged profile access """
    pass


def log_out(session_id: str) -> None:
    """ loggin out a user """
    pass


def reset_password_token(email: str) -> str:
    """ request a reset ppassword token """
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update password """
    pass


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
