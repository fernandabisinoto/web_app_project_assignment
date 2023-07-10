"""
References:

    AuthenticationFailureLoggerModelBackend based on django documentation:

    Django (2023) [online] How to configure and use logging. Available at:
    https://docs.djangoproject.com/en/4.2/howto/logging/ (Accessed: 10 July 2023)
"""

from django.contrib.auth.backends import ModelBackend
import logging

logger = logging.getLogger(__name__)


class AuthenticationFailureLoggerModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is None:
            logger.warning(f"Authentication failure for username: {username}")
        return user
