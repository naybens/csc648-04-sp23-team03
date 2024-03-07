from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse

def logout_view(request):
    if (request.method == 'POST'):
    # Clear the session
        logout(request)
        return HttpResponse('Logging out')
    else:
        return HttpResponse('Failed to log out')