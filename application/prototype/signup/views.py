from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
import json

User = get_user_model()

def signup_view(request):
    return render(request, 'signup/signup.html')

@csrf_protect
def createuser_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        email = data['email']
        password = data['password']
        try:
            validate_email(email)
            validate_password(password)
            try:
                user = User.objects.create(username=username, email=email)
            except IntegrityError:
                raise ValidationError('Username already exists. Please choose a new one!')
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password) # Authenticate the user
            if user is not None:
                login(request, user)  # Log in the user
                return JsonResponse({'session_key': request.session.session_key})
            else:
                return JsonResponse({'error': 'Error logging in'}, status=400)
        except ValidationError as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    return HttpResponse('Invalid request method')
