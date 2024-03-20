from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Record, Redevance
from .models import Fichier

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


# - Register/Create a user

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']


# - Login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# - Create a record

class CreateRecordForm(forms.ModelForm):

    class Meta:

        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country']


# - Update a record

class UpdateRecordForm(forms.ModelForm):

    class Meta:

        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country']

class FichierForm(forms.ModelForm):
    class Meta:
        model = Fichier
        fields = ['nom', 'contenu']

class UpdateRedevanceForm(forms.ModelForm):

    class Meta:

        model = Redevance
        fields = ['airc_type', 'aobt', 'flpl_arrv_airp', 'flpl_call_sign', 'flpl_depr_airp', 'eobt', 'file_date', 'flight_state', 'flight_type', 'ifps_registration_mark', 'initial_flight_rule', 'nm_ifps_id']
