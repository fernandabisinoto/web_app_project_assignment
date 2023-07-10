"""
References:

    SQLInjectionMiddleware based on django documentation:

    Django (2023) [online] How to configure and use logging. Available at:
    https://docs.djangoproject.com/en/4.2/howto/logging/ (Accessed: 10 July 2023)
"""

from django.db import connection
from sql_injection_logger import sql_injection_logger


class SQLInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        queries = connection.queries

        for query in queries:
            if 'DROP' in query['sql'] or 'DELETE' in query['sql']:
                sql_injection_logger.warning(
                    f"Potential SQL injection detected: {query['sql']}"
                )

        return response
