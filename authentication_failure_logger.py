from django.contrib.auth.backends import ModelBackend
import logging

logger = logging.getLogger(__name__)


class AuthenticationFailureLoggerModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is None:
            logger.warning(f"Authentication failure for username: {username}")
        return user
