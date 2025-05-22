# your_app/middleware.py

from django.shortcuts import redirect
from django.urls import reverse
import re
EXEMPT_URLS = [
    r'^/$',  # strona główna
    r'^/accounts/login/?$',         # logowanie
    r'^/accounts/signup/?$',        # rejestracja
    r'^/accounts/logout/?$',        # wylogowanie
    r'^/admin/?$',                  # panel admina
    r'^/accounts/social/login/',           # krok 1 – rozpoczęcie logowania przez Google
    r'^/accounts/google/login/?$',         # krok 2 – kliknięcie w Google login
    r'^/accounts/google/login/callback/?$'
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