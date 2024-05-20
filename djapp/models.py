from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property


# Create your models here.
class MusicTrack(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    mood = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='music/')



class Performer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='performer')
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='performers/')
    bio = models.TextField()

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        # Provide a valid default image URL or path here
        return '/static/default_profile_picture.png'  # Ensure this path is correct and the image exists

    def __str__(self):
        return self.name    

class Performance(models.Model):
    performer = models.ForeignKey('Performer', on_delete=models.CASCADE)
    date = models.DateTimeField()
    details = models.TextField()

    def __str__(self):
        return f"{self.performer.name} on {self.date}"
                 
class SpecialDeal(models.Model):
    title = models.CharField(max_length=255)
    active = models.BooleanField(default=True)  # This field indicates if the deal is currently active

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    
class BarInfo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    social_media_link = models.URLField(max_length=200, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

class CurrentPlaying(models.Model):
    song_title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    performer = models.ForeignKey('Performer', on_delete=models.CASCADE)
    upcoming_songs = models.TextField()  # Store as JSON or plain text
    is_playing = models.BooleanField(default=True)

class Tip(models.Model):
    performer = models.ForeignKey('Performer', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)