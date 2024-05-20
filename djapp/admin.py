from django.contrib import admin
from .models import Performer, MusicTrack
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Performer)
admin.site.register(MusicTrack)
admin.site.register(User, UserAdmin)
        