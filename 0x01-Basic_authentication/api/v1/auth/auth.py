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
            for exPath in excluded_paths:
                if exPath.endswith("*"):
                    if path.startswith(exPath[:-1]):
                        return False
                elif path == exPath:
                    return False
                elif path.rstrip("/") == exPath:
                    return False
                elif path + "/" == exPath:
                    return False
            return True

    def authorization_header(self, request=None) -> str:
        """authorization_header method"""
        if request is None:
            return None
        elif "Authorization" in request.headers:
            return request.headers.get("Authorization")
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method"""
        return None
