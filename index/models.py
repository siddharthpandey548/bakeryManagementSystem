from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Register(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobileno = models.BigIntegerField()


class Category(models.Model):
    cat_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="catimg")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name


class products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desc = models.CharField(max_length=50)
    image = models.ImageField(upload_to="proimg", default="")
    price = models.IntegerField(default=0)
    offer_price = models.BooleanField()

    def __str__(self):
        return self.name


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    update_on = models.DateTimeField(auto_now=True, null=True)


class Order(models.Model):
    cust_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_ids = models.CharField(max_length=250)
    product_ids = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username

    def __str__(self):
        return self.user


class contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    message=models.CharField(max_length=500)
    def __str__(self):
        return self.user

