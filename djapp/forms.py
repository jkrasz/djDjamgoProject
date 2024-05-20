from django import forms
from .models import Performer

class PerformerProfileForm(forms.ModelForm):
    class Meta:
        model = Performer
        fields = ['name', 'profile_picture', 'bio']