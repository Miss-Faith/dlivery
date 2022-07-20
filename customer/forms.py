from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from cloudinary.models import CloudinaryField

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control',}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password', 'name': 'password',}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']

def ForbiddenUsers(value):
  forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
  'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
  if value.lower() in forbidden_users:
    raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
  if '@' in value or '+' in value or '-' in value:
    raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
  if User.objects.filter(email__iexact=value).exists():
    raise ValidationError('User with this email already exists.')

def UniqueUser(value):
  if User.objects.filter(username__iexact=value).exists():
    raise ValidationError('User with this username already exists.')

class RegisterForm(UserCreationForm):
  # fields we want to include and customize in our form
  first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control',}))
  last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control',}))
  username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control',}))
  email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control',}))
  password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password',}))
  password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password',}))

  class Meta:
      model = User
      fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

  def __init__(self, *args, **kwargs):
    super(RegisterForm, self).__init__(*args, **kwargs)
    self.fields['username'].validators.append(ForbiddenUsers)
    self.fields['username'].validators.append(InvalidUser)
    self.fields['username'].validators.append(UniqueUser)
    self.fields['email'].validators.append(UniqueEmail)

  def clean(self):
    super(RegisterForm, self).clean()
    password = self.cleaned_data.get('password')
    confirm_password = self.cleaned_data.get('confirm_password')

    if password != confirm_password:
      self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
    return self.cleaned_data
