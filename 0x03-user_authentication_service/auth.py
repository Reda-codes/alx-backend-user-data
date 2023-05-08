#!/usr/bin/env python
"""
auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Method that takes string arguments and returns bytes """
    salt = b'$2b$12$eUDdeuBtrD41c8dXvzh95eh'
    return bcrypt.hashpw(password.encode(), salt)
