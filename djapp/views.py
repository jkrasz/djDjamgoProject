import logging
import stripe
from django.db import models
from django.shortcuts import render,  redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest,Http404 
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import PerformerProfileForm
from .models import Performer,Performance , SpecialDeal, MusicTrack, SpecialDeal, BarInfo, CurrentPlaying, Tip



logger = logging.getLogger('myapp')
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment_intent(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = data.get("amount")
            if amount is None:
                return HttpResponseBadRequest("Invalid amount")

            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                payment_method_types=["card"],
            )
            return JsonResponse({"clientSecret": intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseBadRequest("Invalid request method")

def tip_performer(request):
    if request.method == 'POST':
        performer_id = request.POST.get('performer_id')
        amount = float(request.POST.get('amount')) * 100  # Stripe expects amount in cents

        performer = get_object_or_404(Performer, id=performer_id)

        intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency='usd',
            metadata={'performer_id': performer_id},
        )

        return render(request, 'djapp/tip_performer.html', {
            'client_secret': intent.client_secret,
            'performers': Performer.objects.all()
        })
    else:
        performers = Performer.objects.all()
        print("Performers:", performers)  # Debugging line
        return render(request, 'djapp/tip_performer.html', {
            'performers': performers,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        })



def owner_dashboard(request):
    performances = Performance.objects.filter(date__gte=timezone.now()).order_by('date')
    performers = Performer.objects.all()
    specials = SpecialDeal.objects.filter(active=True)
    return render(request, 'djapp/owner_dashboard.html', {
        'performances': performances,
        'performers': performers,
        'specials': specials,
    })

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

def customer_dashboard(request):
    bar_info = BarInfo.objects.first()  # Assuming only one bar info object
    current_playing = CurrentPlaying.objects.filter(is_playing=True).first()
    specials = SpecialDeal.objects.filter(active=True)
    return render(request, 'djapp/customer_dashboard.html', {
        'bar_info': bar_info,
        'current_playing': current_playing,
        'specials': specials,
    })


def music_library(request):
    # Assuming you have a model called MusicTrack to represent tracks in your library
    tracks = MusicTrack.objects.all()
    return render(request, 'djapp/music_library.html', {'tracks': tracks})

def bar_specials(request):
    specials = SpecialDeal.objects.filter(active=True)
    return render(request, 'djapp/bar_specials.html', {'specials': specials})

def settings_view(request):
    # Example settings data
    settings_data = {
        'notification_settings': True,  # Suppose this indicates notifications are on
        'profile_visibility': 'Public'
    }
    return render(request, 'djapp/settings.html', {'settings': settings_data})



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
        logger.error(f"No Performer found for the logged-in user: {request.user.username}")
        raise Http404("No Performer found for the logged-in user.")
    

@login_required
def performer_schedule(request):
    try:
        performer = Performer.objects.get(user=request.user)
        performances = Performance.objects.filter(performer=performer).order_by('date')
        return render(request, 'djapp/performer_schedule.html', {
            'performer': performer,
            'performances': performances,
        })
    except Performer.DoesNotExist:
        raise Http404("No Performer found for the logged-in user.")


@login_required
def performer_profile(request):
    try:
        performer = Performer.objects.get(user=request.user)
        return render(request, 'djapp/performer_profile.html', {
            'performer': performer,
        })
    except Performer.DoesNotExist:
        raise Http404("No Performer found for the logged-in user.")

@login_required
def edit_profile(request):
    performer = get_object_or_404(Performer, user=request.user)  # Assuming a relationship exists

    if request.method == 'POST':
        form = PerformerProfileForm(request.POST, instance=performer)
        if form.is_valid():
            form.save()
            return redirect('djapp:performer_dashboard')  # Redirect to the dashboard or appropriate page
    else:
        form = PerformerProfileForm(instance=performer)

    return render(request, 'djapp/edit_profile.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            logger.debug(f"Attempting to authenticate user: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                logger.debug(f"User {username} authenticated successfully")
                login(request, user)
                next_url = request.POST.get('next', 'djapp:performer_dashboard')  # Default redirect if 'next' is not provided
                return redirect(next_url)
            else:
                logger.warning(f"Failed login attempt for user: {username}")
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

