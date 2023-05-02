#!/usr/bin/env python3
"""
BasicAuth class to manage the API authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header method"""
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode_base64_authorization_header method"""
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_en = base64_authorization_header.encode('utf-8')
            base64_de = b64decode(base64_en)
            decoded = base64_de.decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """extract_user_credentials method"""
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':')
        return (credentials[0], credentials[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """user_object_from_credentials method"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            result = User.search({'email': user_email})
            for user in result:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user method"""
        authHeader = self.authorization_header(request)
        b64AuthHdr = self.extract_base64_authorization_header(authHeader)
        decodeAuthHeader = self.decode_base64_authorization_header(b64AuthHdr)
        credentials = self.extract_user_credentials(decodeAuthHeader)
        user = self.user_object_from_credentials(credentials[0],
                                                 credentials[1])
        return user
