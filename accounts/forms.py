from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import *

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class RegisterUserForm(UserCreationForm):
    email = models.EmailField(blank=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]
