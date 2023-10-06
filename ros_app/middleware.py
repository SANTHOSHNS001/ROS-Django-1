# middleware.py

from django.http import HttpResponseRedirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and 'login' not in request.path:
            return HttpResponseRedirect(reverse('login'))
        response = self.get_response(request)
        return response
