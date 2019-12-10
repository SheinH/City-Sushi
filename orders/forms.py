from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import request
from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Visitor, Customer, Review


class CustomerSignUpForm(forms.Form):
    username = forms.CharField(label='Username', min_length=5, max_length=50)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Re-enter password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['f_name', 'l_name', 'phone', 'address']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['f_name', 'l_name', 'phone', 'address']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['dish', 'reviewer', 'rating', 'review_text']
