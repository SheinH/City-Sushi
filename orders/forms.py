from django import forms

from .models import User, Customer, Review


class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_customer = True
            if commit:
                user.save()
            return user


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['f_name',
                  'l_name',
                  # 'phone',
                  'address']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['dish', 'reviewer', 'rating', 'review_text']
