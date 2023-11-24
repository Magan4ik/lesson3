from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        create_profile_url = reverse('accounts:create_profile')
        logout_url = reverse('accounts:logout')

        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            if request.path not in {create_profile_url, logout_url}:
                return redirect(create_profile_url)

        return self.get_response(request)
