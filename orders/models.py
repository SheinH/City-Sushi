from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.db import models


#class User(models.Model):
    #pass

# Added a few more models. Feel free to change this.
# I'll leave the pkey and fkey out for now.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)

class Customer(models.Model):
    f_name = models.CharField(max_length=20,blank=False)
    l_name = models.CharField(max_length=20,blank=False)
    phone = models.CharField(max_length=10,blank=False)
    address = models.TextField()

class Restaurant(models.Model):
    r_name = models.CharField(max_length=100,blank=False)
    info = models.CharField(max_length=100,blank=False)
    location = models.CharField(max_length=50,blank=False)

class Menu(models.Model):
    item_id = models.ForeignKey(Item,on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    quantity = models.IntegerField(blank=False,default=0)


# Replace pass with more data

class Dish(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()


class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User)
    rating = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    review_text = models.TextField(blank=True,null=True)

    def clean(self):
        super().clean()
        if self.rating <= 3 and self.rating is None:
            raise ValidationError('Review required for low rating')
