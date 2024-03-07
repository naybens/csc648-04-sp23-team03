from preferences.models import Preference
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.exceptions import ValidationError

@csrf_protect
@login_required
def userprofile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validate the new email and password
        if email:
            print("email is:", email)
            try:
                validate_email(email)
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            request.user.email = email
        
        if password:
            print("password is:", password)
            try:
                validate_password(password)
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
            request.user.set_password(password)
    
        # Update the user's email and password in the database
        request.user.save()
        update_session_auth_hash(request, request.user) # update session hash value to latest credentials
            
        # Send a JSON response indicating success
        return JsonResponse({'status': 'success'})
    
    return render(request, 'userprofile/profile.html')
