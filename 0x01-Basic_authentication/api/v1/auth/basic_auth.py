#!/usr/bin/env python3
"""
BasicAuth class to manage the API authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extract_base64_authorization_header method"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
