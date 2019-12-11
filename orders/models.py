import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.db import models


class Address(models.Model):
    street_addr = models.CharField("Street Address", max_length=1024)
    city = models.CharField("City", max_length=1024)
    zip_code = models.CharField("ZIP / Postal code", max_length=12)

    def __str__(self):
        return '\n'.join([self.street_addr, f'{self.city} {self.zip_code}'])


class Visitor(models.Model):
    f_name = models.CharField(max_length=100, blank=False, null=False)
    l_name = models.CharField(max_length=100, blank=False, null=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=10, default=0, blank=False, null=False)
    blacklisted = models.BooleanField(default=False)

    def getFullName(self):
        return f'{self.f_name} {self.l_name}'


class Customer(Visitor):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vip = models.BooleanField(default=False)

    # TODO: Add ___str__() method
    # TODO: Investigate whether or not Customer can inherit from User instead of Model

    def __str__(self):
        return self.user.username


class PaymentInfo(models.Model):
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


class Dish(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    def rating(self):
        reviews = self.review_set.all()
        if not reviews:
            return 0
        return sum(x.rating for x in reviews) / len(reviews)


class Order(models.Model):
    vis = models.ForeignKey(Visitor, on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(auto_now_add=True)

    def items(self):
        order_item = OrderItem.objects.filter(order=self)
        return {x.dish: x.quantity for x in order_item}

    def price(self):
        items = self.items()
        price = 0
        for k, v in items.items():
            price += k.price * v
        return price


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


# class Delivery(models.Model):
#     d_f_name = models.CharField(max_length=100, blank=False, null=False)
#     d_l_name = models.CharField(max_length=100, blank=False, null=False)
#     d_phone = models.CharField(max_length=20, blank=False, null=False)
#     rating = models.IntegerField(
#         default=5,
#         validators=[MaxValueValidator(5), MinValueValidator(1)]
#     )
#     review_text = models.TextField(blank=True, null=True)
#     coordinates = models.CharField(max_length=10, blank=False, null=False)
#     bid = models.ForeignKey(Manager, on_delete=models.DO_NOTHING)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.d_f_name} {self.d_l_name}: phone number {self.d_phone}'
#
#     def rating(self):
#         reviews = self.review_set.all()
#         return sum(x.rating for x in reviews) / len(reviews)
class Deliverer(models.Model):
    f_name = models.CharField(max_length=100, blank=False, null=False)
    l_name = models.CharField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=10, default=0, blank=False, null=False)


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
