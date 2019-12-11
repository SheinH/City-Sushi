from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Visitor, Customer, Review, PaymentInfo


class CustomerSignUpForm(forms.Form):
    username = forms.CharField(label='Username', min_length=5, max_length=20)
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

    def clean_password_confirm(self):
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


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', min_length=5, max_length=20)
    shipping = forms.CharField(label="Shipping Address", max_length=200)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Re-enter password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if r:
            raise ValidationError("Username already exists")
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords don't match")

        return password_confirm

    class Meta:
        model = Customer
        fields = ['f_name', 'l_name', 'email', 'phone']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['name', 'card_num', 'exp_month', 'exp_year', 'cvv']


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['f_name', 'l_name', 'phone']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['f_name', 'l_name', 'phone']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['dish', 'reviewer', 'rating', 'review_text']
