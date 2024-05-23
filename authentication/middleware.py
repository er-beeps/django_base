# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user.is_password_changed is False:
            if(request.get_full_path() != '/password_change/'):
                return redirect('auth:password_change')

        response = self.get_response(request)
        return response
