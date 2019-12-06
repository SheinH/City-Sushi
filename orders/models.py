from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.db import models


# IMPORTANT NOTE: Django already has built-in User
# We will not create our own and we will use django's user

# Added a few more models. Feel free to change this.
# I'll leave the pkey and fkey out for now.

# I think customer can inherit from User but i'm not sure
# class Customer(User): might be better

class Customer(models.Model):
    f_name = models.CharField(max_length=20, blank=False)
    l_name = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    address = models.TextField()
    # TODO: Add ___str__() method
    # TODO: Investigate whether or not Customer can inherit from User instead of Model


class Restaurant(models.Model):
    r_name = models.CharField(max_length=100, blank=False)
    info = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=50, blank=False)
    # TODO: Add ___str__() method


class Menu(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False, default=0)
    # TODO: Add ___str__() method


# Replace pass with more data

class Dish(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return self.name

    def rating(self):
        reviews = self.review_set.all()
        return sum(x.rating for x in reviews) / len(reviews)


class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    review_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.reviewer}: {self.rating} stars'

    def clean(self):
        super().clean()
        if self.rating <= 3 and self.rating is None:
            raise ValidationError('Review required for low rating')
