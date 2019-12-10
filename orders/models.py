from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.db import models


class Visitor(models.Model):
    f_name = models.CharField(max_length=100, blank=False, null=False)
    l_name = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    email = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=10, default=0, blank=False, null=False)
    blacklisted = models.BooleanField(default=False)

    def getFullName(self):
        return f'{self.f_name} {self.l_name}'


class Customer(Visitor):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # TODO: Add ___str__() method
    # TODO: Investigate whether or not Customer can inherit from User instead of Model

    def __str__(self):
        return self.user.username


class Payment_Info(models.Model):
    name = models.CharField(max_length=200, blank=False)
    card_num = models.IntegerField(default=0)
    exp_month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    exp_year = models.IntegerField(
        validators=[MinValueValidator(19)]
    )
    cvv = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(999)]
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


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

    # bid = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.d_f_name} {self.d_l_name}: phone number {self.d_phone}'

    def rating(self):
        reviews = self.review_set.all()
        return sum(x.rating for x in reviews) / len(reviews)


class Dish(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return self.name

    def rating(self):
        reviews = self.review_set.all()
        if not reviews:
            return 0
        return sum(x.rating for x in reviews) / len(reviews)


class Order(models.Model):
    pass
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish_name

    def rating(self):
        reviews = self.review_set.all()
        print(reviews)
        print(len(reviews))
        if not reviews:
            return 0
        else:
            return sum(x.rating for x in reviews) / len(reviews)


class OrderItem(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # cook = models.ForeignKey(Cook, on_delete=models.DO_NOTHING)
    # inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING)
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
