from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from djapp.models import Performer, Performance
import logging

logger = logging.getLogger(__name__)

logout_view = LogoutView.as_view()

#   @login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            logger.info(f"Attempting to authenticate user: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logger.info(f"User {username} authenticated successfully")
                login(request, user)
                next_url = request.POST.get('next', 'djapp:performer_dashboard')  # Default redirect if 'next' is not provided
                return redirect(next_url)
            else:
                logger.warning(f"Failed login attempt for user: {username}")
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def performer_dashboard(request):
    try:
        performer = Performer.objects.get(user=request.user)
        upcoming_performances = Performance.objects.filter(performer=performer, date__gte=timezone.now())
        return render(request, 'djapp/performer_dashboard.html', {
            'performer': performer,
            'upcoming_performances': upcoming_performances,
        })
    except Performer.DoesNotExist:
        raise Http404("No Performer found for the logged-in user.")

def home(request):
    return render(request, 'home.html')