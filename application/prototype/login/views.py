from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
import json

def login_view(request):
    return render(request, 'login/login.html')

def getUserToken(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:         
            token = Token.objects.get_or_create(user=user)[0]
            login(request, user)
            return JsonResponse({'token': token.key, 'session_key': request.session.session_key})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
    else:
        return HttpResponse('Invalid request method')