from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    sub_name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    size = models.CharField(max_length=600)
    category = models.CharField(max_length=200)
    price = models.FloatField()

class Extras(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()

class ProductExtras(models.Model):
    product_id = models.IntegerField(max_length=50)
    extra_id = models.IntegerField(max_length=50)

class UtilityData(models.Model):
    name = models.CharField(max_length=200)
    info = models.CharField(max_length=200)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=3000)
    total = models.FloatField()
    paymentType = models.CharField(max_length=200)
    deliveryType = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    email = models.EmailField()
    date = models.DateTimeField()
    comment = models.CharField(max_length=300)
    option = models.CharField(max_length=600)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    type = models.CharField(max_length=200)

class OptionCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

class Options(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(OptionCategory)

class ProductOption(models.Model):
    product = models.ForeignKey(Product)
    optionCategory = models.ForeignKey(OptionCategory)
    maxNumOptions = models.CharField(max_length=6)