# your_app/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
import re
EXEMPT_URLS = [
    r'^/$',  # strona główna
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if not request.user.is_authenticated:
            if not any(re.match(pattern, path) for pattern in EXEMPT_URLS):
                return redirect('/')
        return self.get_response(request)