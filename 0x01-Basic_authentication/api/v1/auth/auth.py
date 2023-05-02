#!/usr/bin/env python3
"""
Auth class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth method"""
        if path is None or excluded_paths is None:
            return True
        else:
            if path in excluded_paths:
                return False
            elif path.rstrip("/") in excluded_paths:
                return False
            elif path + "/" in excluded_paths:
                return False
            else:
                return True

    def authorization_header(self, request=None) -> str:
        """authorization_header method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method"""
        return None