#!/usr/bin/env python3
""" encrypt_password file """
import bcrypt


def hash_password(password: str) -> bytes:
    """function that takes a string (password) and returns a salted,
    hashed password, which is a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
