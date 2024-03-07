from django.shortcuts import render
# Uncomment if we need to use hardcode example
# from django.contrib.auth.models import User
from preferences.models import History
from django.contrib.auth.decorators import login_required


@login_required
def render_search_history(request):
    # Configs
    number_of_search_result = 5

    user = request.user
    # user = User.objects.get(username='bierman9000') # Hardcode example

    # Gives the 5 latest search results
    latest_history = History.objects.filter(user=user).order_by(
        '-creation_datetime')[:number_of_search_result]

    context = {'latest_history': latest_history}
    return render(request, 'searchhistory/latest_history.html', context)
