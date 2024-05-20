from django.urls import path
from . import views
from .views import login_view
app_name = 'accounts'  # Setting the namespace for the app

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]   

