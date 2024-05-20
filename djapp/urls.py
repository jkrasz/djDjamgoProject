from django.urls import path
from . import views

app_name = 'djapp'  # Setting the namespace for the app


urlpatterns = [
    path('performers/', views.performer_dashboard, name='performer_dashboard'),
    path('performers/schedule/', views.performer_schedule, name='performer_schedule'),  # Added performer_schedule URL
    path('performers/profile/', views.performer_profile, name='performer_profile'),  # Added performer_profile URL
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('music-library/', views.music_library, name='music_library'),
    path('bar-specials/', views.bar_specials, name='bar_specials'),
    path('settings/', views.settings_view, name='settings'),
    path('performers/edit-profile/', views.edit_profile, name='edit_profile'),  # New URL for editing performer profiles
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/tip/', views.tip_performer, name='tip_performer'),
    path('customer/create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
]