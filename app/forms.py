from django import forms
from .models import College
from .models import Event
# forms.py

class AdminSignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length = 100)
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class StudentSignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    roll_number = forms.IntegerField()
    name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    

class ParticipantSignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100)
    college = forms.ModelChoiceField(queryset=College.objects.all())  # Dropdown menu for selecting college

class OrganizerSignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100)
    #college = forms.ModelChoiceField(queryset=College.objects.all())
    event = forms.ModelChoiceField(queryset=Event.objects.all())
class RegistrationForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput)

class StudentRegistrationForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput)
    registration_type = forms.ChoiceField(choices=(('participant', 'Participant'), ('volunteer', 'Volunteer')), label='Registration Type')

