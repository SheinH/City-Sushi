from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.db import models


class Restaurant(models.Model):
    r_name = models.CharField(max_length=100, blank=False, null=False)
    info = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.r_name


class Manager(models.Model):
    m_name = models.CharField(max_length=50, blank=False, null=False)
    m_email = models.CharField(max_length=50, blank=False, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.r_name


class Delivery(models.Model):
    d_f_name = models.CharField(max_length=100, blank=False, null=False)
    d_l_name = models.CharField(max_length=100, blank=False, null=False)
    d_phone = models.CharField(max_length=20, blank=False, null=False)
    rating = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    review_text = models.TextField(blank=True, null=True)
    coordinates = models.CharField(max_length=10, blank=False, null=False)
    bid = models.ForeignKey(Manager, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.d_f_name} {self.d_l_name}: phone number {self.d_phone}'

    def rating(self):
        reviews = self.review_set.all()
        return sum(x.rating for x in reviews) / len(reviews)


class Sales(models.Model):
    s_name = models.CharField(max_length=50, blank=False, null=False)
    commission = models.IntegerField(default=0, blank=False, null=False)
    warning = models.IntegerField(default=3,
                                  validators=[MaxValueValidator(3), MinValueValidator(0)])
    s_laid_off = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.s_name


class Inventory(models.Model):
    i_name = models.CharField(max_length=50, blank=False, null=False)
    time_stored = models.IntegerField(default=0, blank=False, null=False)
    amount = models.IntegerField(default=0, blank=False, null=False)
    rating = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    restaurant = models.ManyToManyField(Sales)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.i_name

    def rating(self):
        reviews = self.review_set.all()
        return sum(x.rating for x in reviews) / len(reviews)


class Cook(models.Model):
    c_name = models.CharField(max_length=50, blank=False, null=False)
    commission = models.IntegerField(default=0, blank=False, null=False)
    warning = models.IntegerField(default=3,
                                  validators=[MaxValueValidator(3), MinValueValidator(0)])
    c_laid_off = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.c_name
