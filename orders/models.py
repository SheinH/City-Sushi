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

class Visitor(models.Model):
    f_name = models.CharField(max_length=100, blank=False, null=False)
    l_name = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False)
    blacklisted = models.BooleanField(default=False)

    def getFullName(self):
        return f'{self.f_name} {self.l_name}'


class Customer(Visitor):
    address = models.TextField()
    # TODO: Add ___str__() method
    # TODO: Investigate whether or not Customer can inherit from User instead of Model


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


class Restaurant(models.Model):
    r_name = models.CharField(max_length=100, blank=False, null=False)
    info = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.r_name


class Manager(models.Model):
    m_name = models.CharField(max_length=50)
    m_email = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.r_name


class Sales(models.Model):
    s_name = models.CharField(max_length=50)
    commission = models.IntegerField(default=0)
    warning = models.IntegerField(default=3,
        validators=[MaxValueValidator(3), MinValueValidator(0)])
    s_laid_off = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.s_name


class Cooks(models.Model):
    c_name = models.CharField(max_length=50)
    commission = models.IntegerField(default=0)
    warning = models.IntegerField(default=3,
        validators=[MaxValueValidator(3), MinValueValidator(0)])
    c_laid_off = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    # TODO: ADD RATING/REVIEW CONNECTIONS

    def __str__(self):
        return self.c_name


class Inventory(models.Model):
    i_name = models.CharField(max_length=50)
    time_stored = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    restaurant = models.ManyToManyField(Sales)

    # TODO: ADD RATING CONNECTIONS

    def __str__(self):
        return self.i_name




class Customer(models.Model):
    f_name = models.CharField(max_length=20, blank=False, null=False)
    l_name = models.CharField(max_length=20, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    address = models.TextField()
    # TODO: Add ___str__() method
    # TODO: Investigate whether or not Customer can inherit from User instead of Model


class Payment_Info(models.Model):
    bank = models.CharField(max_length=50, blank=False)
    card_num = models.IntegerField(default=0)
    exp_date = models.DateField()
    cvv = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

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
    cook = models.ForeignKey(Cooks, on_delete=models.DO_NOTHING)
    inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING)
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


